import torch
# import torch.nn as nn
import torch.optim
import torch.distributed
# from torch.nn.parallel import DistributedDataParallel as DDP
import torch.multiprocessing
import numpy as np
import os
# from collections import OrderedDict
# from ddp_model import NerfNet
import time
from data_loader_split import load_data_split
from utils import mse2psnr, colorize_np, to8b
import imageio
from ddp_train_nerf import config_parser, setup_logger, setup, cleanup, render_single_image, create_nerf
import logging
from collections import OrderedDict


logger = logging.getLogger(__package__)


# https://developers.google.com/vr/jump/rendering-ods-content.pdf
def render_ods_image(is_left_eye, IPD, H, W):
    
    u, v = np.meshgrid(np.arange(W), np.arange(H))

    u = u.reshape(-1).astype(dtype=np.float32)
    v = v.reshape(-1).astype(dtype=np.float32)
    # print("Input dimensions ", v.shape, (v >= (H/2)).shape)
    v[(v >= (H/2))] -= (H/2)

    # print("Values less than zero ", np.sum(np.abs(v[v<=0])))
    u = (u + 0.5) / W   # add half pixel
    v = (v + 0.5) * 2 / H
    # ODS image is equirectangular (spherical) with U ranging from (-180, 180) degree 
    # and V ranging from (-90, 90) degree
    pixels = np.stack((u, v, np.ones_like(u)), axis=0)  # (3, H*W)
    theta = 2*np.pi*u - np.pi
    # phi = np.pi / 2 - v * np.pi
    phi = v * np.pi - (np.pi / 2)
    if(is_left_eye):
        scale = -1*IPD/2
    else:
        scale = IPD/2
    
    ray_origin = np.vstack([np.cos(theta), np.zeros(theta.shape[0]), \
        np.sin(theta)]).transpose() * scale
    # Ray directions are tangent to the circle.
    ray_direction = np.vstack([np.sin(theta)*np.cos(phi), np.sin(phi), 
        -1*np.cos(theta)*np.cos(phi)]).transpose()

    # print("Output dimensions ", ray_origin.shape, ray_direction.shape)
    # print(ray_origin[:10], ray_direction[:10])
    ray_origin = torch.from_numpy(ray_origin)
    ray_direction = torch.from_numpy(ray_direction)
    min_depth = torch.from_numpy(1e-4 * np.ones_like(ray_direction[..., 0]))
    ret = OrderedDict([
            ('ray_o', ray_origin.float()),
            ('ray_d', ray_direction.float()),
            ('min_depth', min_depth.float())
            ])
    return ret


class RaySamplerSingleImage(object):
    def __init__(self, H = 2048, W = 2048, IPD = 0.06):
        super().__init__()
        self.W_orig = W
        self.H_orig = H
        self.IPD = IPD
        is_left_eye = True

        self.W = self.W_orig 
        self.H = self.H_orig 

        self.ray_samp = render_ods_image(True, IPD, H, W)

    # def set_eye_pos(self, is_left):
    #     self.is_left = is_left

    def set_camera_pos(self, cam_offset):
        self.ray_frm_cam = OrderedDict([
            ('ray_o', torch.clone(self.ray_samp['ray_o']) + torch.FloatTensor(cam_offset)),
            # ('ray_d', torch.clone(self.ray_samp['ray_d']) + torch.FloatTensor(cam_offset)),
            ('ray_d', self.ray_samp['ray_d']),
            ('min_depth', self.ray_samp['min_depth'])
            ])
        return

    def get_all(self):
        return self.ray_frm_cam
        


def ddp_test_nerf(rank, args):
    ###### set up multi-processing
    setup(rank, args.world_size)
    ###### set up logger
    logger = logging.getLogger(__package__)
    setup_logger()

    ###### decide chunk size according to gpu memory
    if torch.cuda.get_device_properties(rank).total_memory / 1e9 > 14:
        logger.info('setting batch size according to 24G gpu')
        args.N_rand = 1024
        args.chunk_size = 2*8192
    else:
        logger.info('setting batch size according to 12G gpu')
        args.N_rand = 512
        args.chunk_size = 4096

    ###### create network and wrap in ddp; each process should do this
    start, models = create_nerf(rank, args)

    out_dir = os.path.join(args.basedir, args.expname, 'render_ods')
    if rank == 0:
        os.makedirs(out_dir, exist_ok=True)


    ods_ray_sampler = RaySamplerSingleImage()
    
    NUM_FRMS = 10
    for i in range(NUM_FRMS):
        fname = "ods_output_" + str(i) + ".png"
        theta = 2.0*np.pi*i/NUM_FRMS
        offset = [0.3*np.cos(theta), 0.03, 0.3*np.sin(theta)]
        ods_ray_sampler.set_camera_pos(offset)

        time0 = time.time()
        ret = render_single_image(rank, args.world_size, models, ods_ray_sampler, args.chunk_size)
        dt = time.time() - time0
        if rank == 0:    # only main process should do this
            logger.info('Rendered {} in {} seconds'.format(fname, dt))

            # only save last level
            im = ret[-1]['rgb'].numpy()

            im = to8b(im)
            imageio.imwrite(os.path.join(out_dir, fname), im)

            im = ret[-1]['fg_rgb'].numpy()
            im = to8b(im)
            imageio.imwrite(os.path.join(out_dir, 'fg_' + fname), im)

            im = ret[-1]['bg_rgb'].numpy()
            im = to8b(im)
            imageio.imwrite(os.path.join(out_dir, 'bg_' + fname), im)

            im = ret[-1]['fg_depth'].numpy()
            im = colorize_np(im, cmap_name='jet', append_cbar=True)
            im = to8b(im)
            imageio.imwrite(os.path.join(out_dir, 'fg_depth_' + fname), im)

            im = ret[-1]['bg_depth'].numpy()
            im = colorize_np(im, cmap_name='jet', append_cbar=True)
            im = to8b(im)
            imageio.imwrite(os.path.join(out_dir, 'bg_depth_' + fname), im)

    torch.cuda.empty_cache()

    # clean up for multi-processing
    cleanup()


def test():
    parser = config_parser()
    args = parser.parse_args()
    logger.info(parser.format_values())

    if args.world_size == -1:
        args.world_size = torch.cuda.device_count()
        logger.info('Using # gpus: {}'.format(args.world_size))
    torch.multiprocessing.spawn(ddp_test_nerf,
                                args=(args,),
                                nprocs=args.world_size,
                                join=True)


if __name__ == '__main__':
    setup_logger()
    test()
    # is_left_eye = True
    # IPD = 0.6
    # H = 2048
    # W = 2048
    # ray_origin, ray_direction = render_ods_image(is_left_eye, IPD, H, W)


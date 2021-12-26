import time
import datetime
import torch
import tqdm
from torch.nn import DataParallel
from lib.config import cfg
import torch
import torch.nn as nn
from torchvision.models import resnet50
from torchvision.models.segmentation import fcn_resnet50, deeplabv3_resnet101
import numpy as np
from spconv.pytorch.utils import PointToVoxel, gather_features_by_pc_voxel_id
from collections import OrderedDict
from torch import distributed as dist



def get_feat_gen_net():
    # resnet = resnet50(pretrained = True)
    resnet = fcn_resnet50(pretrained = True)
    # print("train_nodes ", rank)
    # print("Model layers ", list(resnet.children())[:-2], len(list(resnet.children())))

    modules = list(resnet.children())[:-2] # delete the last two layers.
    # modules = list(resnet.children())

    resnet = nn.Sequential(*modules)

    ### Now set requires_grad to false
    for param in resnet.parameters():
        param.requires_grad = False

    # resnet = DDP(resnet, device_ids=[rank], output_device=rank, find_unused_parameters=True)


    return resnet

def bbox2vox_dim(bbox, voxel_size):
    vox_min, vox_max = bbox #bbox[:3], bbox[3:]
    steps = np.floor(((vox_max - vox_min) / voxel_size)).astype('int64') + 1

    vox_min = vox_min # - (voxel_size/2.0)
    vox_max = vox_min + (steps) * voxel_size
    # print("Num steps ", steps, bbox, voxel_size, vox_min, vox_max)

    return steps, vox_min, vox_max

# def bbox2voxels(bbox, voxel_size):
#     vox_min, vox_max = bbox #bbox[:3], bbox[3:]
#     steps = ((vox_max - vox_min) / voxel_size).round().astype('int64') + 1
#     # print("Num steps ", steps, bbox, voxel_size)

#     x, y, z = [c.reshape(-1).astype('float32') for c in np.meshgrid(np.arange(steps[0]), np.arange(steps[1]), np.arange(steps[2]))]
#     x, y, z = x * voxel_size + vox_min[0], y * voxel_size + vox_min[1], z * voxel_size + vox_min[2]


    return torch.from_numpy(np.stack([x, y, z]).T.astype('float32'))

def cal_bbox_frm_cam_bbox(cam_bbox):
    vox_min, vox_max = cam_bbox
    mid_point = (vox_max + vox_min)/2
    max_dim = np.max(vox_max - vox_min)/2
    bbox_min = mid_point - max_dim
    bbox_max = mid_point + max_dim
    return bbox_min, bbox_max


# def cal_vox_idx(ray_o, ray_d, depth, voxel_size, bbox):

#     # Calculate the feature coordinate
#     feat_wc = ray_o + depth*ray_d
#     feat_wc = feat_wc[depth != 0]
#     gen = PointToVoxel(
#         vsize_xyz=[voxel_size, voxel_size, voxel_size], 
#         coors_range_xyz=[-80, -80, -2, 80, 80, 6], 
#         num_point_features=3, 
#         max_num_voxels=5000, 
#         max_num_points_per_voxel=5)
#     return

# Convert rays to vox_idx
def get_vox_idx(ray_o, ray_d, depth, vox_min, voxel_size, vox_steps, img_feat):
    img_idx = (depth != 0)
    # print("Input shapes B", img_feat.shape, ray_o.shape, ray_d.shape, depth.shape)

    img_feat = img_feat[img_idx, :]
    # Convert it to (x, y, z)
    point_cloud = ray_o[img_idx] + ray_d[img_idx]*depth[img_idx].unsqueeze(-1)
    vox_idx = ((point_cloud - vox_min)/voxel_size).round().to(torch.long)
    # print("Vox values ", vox_idx.shape, vox_idx[:10],
    #     point_cloud[:10], vox_min, voxel_size)
    # print(ray_o[img_idx][:10],ray_d[img_idx][:10],depth[img_idx][:10])
    # print("Input shapes ", img_feat.shape, ray_o.shape, ray_d.shape, 
    #     depth.shape, vox_idx.shape)
    vox_filt = torch.logical_and(
                torch.logical_and(vox_idx[:, 0] < vox_steps[0], 
                    vox_idx[:, 1] < vox_steps[1]), 
                vox_idx[:, 2] < vox_steps[2])

    vox_idx = vox_idx[vox_filt, :]
    img_feat = img_feat[vox_filt, :]

    # print("Input shapes A", vox_idx.shape, img_feat.shape, vox_steps)
    # print("Vox idx B", vox_idx[:10])
    vox_idx_1 = vox_steps[1]*vox_steps[0]*vox_idx[:, 2] + \
        vox_steps[0]*vox_idx[:, 1] + vox_idx[:, 0]

    # vox_xyz = vox_idx_to_vox_xyz(vox_idx_1, vox_steps)
    # print("Vox xyz ", vox_xyz[:10], vox_idx[:10], vox_steps)

    # if torch.equal(vox_xyz.int(), vox_idx):
    #     idx = vox_xyz.int() != vox_idx
    #     print("Error error pants on fire")
    #     print(idx.sum())
    #     print(vox_idx[idx])
    #     print(vox_xyz.int()[idx])


    # print("Voxel idx ", vox_idx[:20], vox_idx.shape)

    return vox_idx_1, img_feat, point_cloud

def vox_idx_to_vox_xyz(vox_idx, vox_steps):
    vox_z = (vox_idx/(vox_steps[1]*vox_steps[0])).floor()
    vox_y = ((vox_idx - vox_z*vox_steps[1]*vox_steps[0])/vox_steps[0]).floor()
    vox_x = vox_idx - vox_z*vox_steps[1]*vox_steps[0] - vox_y*vox_steps[0]
    vox_xyz = torch.stack([vox_x, vox_y, vox_z]).T
    # print("Vox_xyz ", vox_xyz[:10, 0], vox_x[:10], vox_y[:10], vox_z[:10])
    return vox_xyz

class FeatGen(object):
    def __init__(self, cam_bbox, voxel_size):
        device = torch.device('cuda:{}'.format(cfg.local_rank))
        self.feat_gen_net = get_feat_gen_net().to(device)
        # if cfg.distributed:
        #     feat_gen_net = torch.nn.parallel.DistributedDataParallel(
        #         feat_gen_net,
        #         device_ids=[cfg.local_rank],
        #         output_device=cfg.local_rank
        #     )
        self.local_rank = cfg.local_rank
        self.device = device
        bbox = cal_bbox_frm_cam_bbox(cam_bbox)
        bbox_min, bbox_max = bbox

        # self.vox_vol = bbox2voxels(bbox, voxel_size).to(self.device)

        self.feat_size = 2048
        steps, vox_min, vox_max = bbox2vox_dim(bbox, voxel_size)
        num_vox = steps[0]*steps[1]*steps[2]
        self.sum_feat = torch.zeros(num_vox, self.feat_size).to(device)
        self.sum_sqr_feat = torch.zeros(num_vox, self.feat_size).to(device)
        self.num_feat = torch.zeros(num_vox).to(device)
        self.vox_steps = torch.from_numpy(steps).to(device)
        self.vox_min = torch.from_numpy(vox_min).to(device)
        self.vox_max = torch.from_numpy(vox_max).to(device)
        self.voxel_size = voxel_size#.to(device)

        # self.point2vox = PointToVoxel(
        #     vsize_xyz=[voxel_size, voxel_size, voxel_size], 
        #     coors_range_xyz=[bbox_min[0], bbox_min[1], bbox_min[2], \
        #         bbox_max[0], bbox_max[1], bbox_max[2]], 
        #     num_point_features=3, 
        #     max_num_voxels=5000, 
        #     max_num_points_per_voxel=5)


    def to_cuda(self, batch):
        for k in batch:
            if k == 'meta':
                continue
            if isinstance(batch[k], tuple) or isinstance(batch[k], list):
                batch[k] = [b.to(self.device) for b in batch[k]]
            else:
                batch[k] = batch[k].to(self.device)
        return batch

    def gen_feat_volume(self, data_loader, recorder):
        max_iter = len(data_loader)

        end = time.time()
        # self.point_cloud = np.empty( shape=(0, 3) )
        for iteration, batch in enumerate(data_loader):
            data_time = time.time() - end
            iteration = iteration + 1

            batch = self.to_cuda(batch)
            img_feat = self.feat_gen_net(batch['image'])['out'] # out, aux - Two outputs possible
            # print("Image features keys ", img_feat.shape)

            img_feat_sh = img_feat.shape
            img_feat = img_feat.permute(0,2,3,1).reshape(img_feat.shape[0], 
                -1, self.feat_size)
            # print("Image feature shape ", img_feat_sh, img_feat.shape)


            vox_idx, img_feat, pc = get_vox_idx(batch['ray_o'], batch['ray_d'], batch['depth'], \
                self.vox_min, self.voxel_size, self.vox_steps, img_feat)

            self.sum_feat[vox_idx, :] += img_feat
            self.sum_sqr_feat[vox_idx, :] += (img_feat**2)
            self.num_feat[vox_idx] += 1
            # self.point_cloud = \
            #     np.append( self.point_cloud, pc.cpu().detach().numpy(), axis=0)
            # print("Output shape ", img_feat.shape,
            #     torch.sum(batch['depth']==0))

            # print("total num features ", iteration, vox_idx.shape,
            #     torch.max(self.num_feat), torch.argmax(self.num_feat),
            #     (self.num_feat == iteration).nonzero().shape,
            #     (self.num_feat != 0).nonzero().shape)

            # exit(-1)


            if cfg.local_rank > 0:
                continue

            batch_time = time.time() - end
            end = time.time()
            recorder.feat_gen_bat_time.update(batch_time)
            recorder.feat_gen_dat_time.update(data_time)

            if iteration % cfg.log_interval == 0 or iteration == (max_iter - 1):
                # print training state
                eta_seconds = recorder.feat_gen_bat_time.global_avg * (max_iter - iteration)
                eta_string = str(datetime.timedelta(seconds=int(eta_seconds)))
                # lr = optimizer.param_groups[0]['lr']
                memory = torch.cuda.max_memory_allocated() / 1024.0 / 1024.0

                feat_gen_state = '  '.join(['eta: {}', 'max_mem: {:.0f}'])
                feat_gen_state = feat_gen_state.format(eta_string, memory)
                print(feat_gen_state)

            # if iteration % cfg.record_interval == 0 or iteration == (max_iter - 1):
            #     # record loss_stats and image_dict
            #     recorder.update_image_stats(image_stats)
            #     recorder.record('train')
        if cfg.distributed:
            dist.all_reduce(self.sum_feat, op=dist.ReduceOp.SUM)
            dist.all_reduce(self.sum_sqr_feat, op=dist.ReduceOp.SUM)
            dist.all_reduce(self.num_feat, op=dist.ReduceOp.SUM)


    def get_vol_feat(self):
        # if(cfg.local_rank > 0):
        #     return

        min_num_feat = 10
        vox_idx = (self.num_feat > min_num_feat)
        mean_feat = self.sum_feat[vox_idx, :] / self.num_feat[vox_idx].unsqueeze(-1)
        mean_sqr_feat = self.sum_sqr_feat[vox_idx, :] / self.num_feat[vox_idx].unsqueeze(-1)
        var_feat = mean_sqr_feat - mean_feat*mean_feat
        num_feat = self.num_feat[vox_idx]
        # print("Num valid features ", torch.min(self.num_feat), 
        #     torch.max(self.num_feat), torch.sum(vox_idx), 
        #     self.vox_steps[0]*self.vox_steps[1]*self.vox_steps[2])
        # print(self.num_feat[vox_idx][:15])
        coord = vox_idx_to_vox_xyz(
            torch.arange(self.num_feat.shape[0])[vox_idx].to(self.device), 
            self.vox_steps)
        bat_idx = torch.full([coord.shape[0]], 0).to(coord)
        # coord = batch['coord'].view(-1, sh[-1])
        coord = torch.cat([bat_idx[:, None], coord], dim=1).to(torch.int32)
        # coord = coord[vox_idx]

        # Filtering based on variance
        var_sum = torch.sum(torch.abs(var_feat), axis=-1)
        var_sum_idx = var_sum < 100
        coord_high_var = coord[var_sum >= 100]
        mean_feat = mean_feat[var_sum_idx]
        var_feat = var_feat[var_sum_idx]
        num_feat = num_feat[var_sum_idx]
        coord = coord[var_sum_idx]



        # np.save('point_cloud_'+str(cfg.local_rank), self.point_cloud)
        # print("Point cloud ", cfg.local_rank, self.point_cloud.shape)

        if cfg.local_rank == 0:
            num_val_to_print = 30
            var_sum = torch.sum(torch.abs(var_feat), axis=-1)

            print("Volume features ")
            print(num_feat[:num_val_to_print])
            print(torch.sum(torch.abs(mean_feat), axis=-1)[:num_val_to_print])
            print(torch.sum(torch.abs(var_feat), axis=-1)[:num_val_to_print])
            print(coord[:num_val_to_print])
            print(torch.sum(vox_idx), torch.sum(var_sum_idx))
            print(self.vox_steps)
            print(torch.min(self.num_feat), torch.max(self.num_feat))

            mean_feat_np = mean_feat.cpu().detach().numpy()
            var_feat_np = var_feat.cpu().detach().numpy()
            coord_np = coord.cpu().detach().numpy()
            num_feat_np = num_feat.cpu().detach().numpy()
            coord_high_var_np = coord_high_var.cpu().detach().numpy()

            np.save('mean_feat_np', mean_feat_np)
            np.save('var_feat_np', var_feat_np)
            np.save('coord_np', coord_np)
            np.save('num_feat_np', num_feat_np)
            np.save('coord_high_var_np', coord_high_var_np)
            




        # code, coord, out_sh, batch_size
        ret = OrderedDict([
            ('mean_feat', mean_feat),
            ('var_feat', var_feat),
            ('out_sh', self.vox_steps),
            ('num_feat', num_feat),
            # ('batch_size', torch.sum(vox_idx)),
            ('coord', coord),
            ('vox_min', self.vox_min)
        ])
        return ret

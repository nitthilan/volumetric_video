#!/usr/bin/env python3

import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np
import pytorch_lightning as pl
import json
import volume_rendering as vr
# from torch_ema import ExponentialMovingAverage
from torchvision.utils import save_image
from torchvision.transforms import ToPILImage
from clib import (
    aabb_ray_intersect, triangle_ray_intersect, svo_ray_intersect,
    uniform_ray_sampling, inverse_cdf_sampling
)

import camera_pose as cpose
import losses


try:
    import tinycudann as tcnn
except ImportError:
    print("This sample requires the tiny-cuda-nn extension for PyTorch.")
    print("You can install it by running:")
    print("============================================================")
    print("tiny-cuda-nn$ cd bindings/torch")
    print("tiny-cuda-nn/bindings/torch$ python setup.py install")
    print("============================================================")
    sys.exit()

def dump_image(rgb, name, wth=int(1920/4), hgt=int(1440/4)):
    rgb = rgb.detach()
    rgb = rgb.reshape(hgt, wth, -1)
    rgb = torch.transpose(rgb, 0, 2)
    rgb = ToPILImage()(rgb)
    rgb.save(name)
    # save_image(rgb, 'rgb' + str(idx) + '.png')
    return

class NVSEnc(pl.LightningModule):

    def __init__(self, config_path, num_frames, voxel_size, voxel_base_xyz,
        box_min_off, box_dim, max_hits, resolution_level,
        sc_factor, truncation, max_depth):
        super().__init__()

        with open(config_path) as config_file:
            config = json.load(config_file)

        self.n_den_inp = 3 # num channels of input density
        self.n_den_out = 16 # density network output channels
        self.den_net = tcnn.NetworkWithInputEncoding(self.n_den_inp, 
            self.n_den_out, encoding_config=config["encoding"], 
            network_config=config["network"])

        self.n_dir_inp = 3
        self.n_rgb_out = 3
        self.rgb_enc = tcnn.Encoding(self.n_dir_inp, config["dir_encoding"])
        n_rgb_inp = self.rgb_enc.n_output_dims + self.n_den_out #+ frm_emb_dim
        self.rgb_net = tcnn.Network(n_rgb_inp, self.n_rgb_out, config["rgb_network"])
        print(self.den_net)
        print(self.rgb_enc)
        print(self.rgb_net)
        # print(self.rgb_enc.n_output_dims, )

        # frm_emb_dim = 16
        # self.frm_emb = nn.Embedding(num_frames, frm_emb_dim)
        pose_emb_size = 6
        self.pose_cor_emb = nn.Embedding(num_frames, pose_emb_size)
        self.pose_cor_emb.weight = torch.nn.Parameter(torch.zeros(num_frames, pose_emb_size))

        self.config = config
        # self.optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        self.params = list(self.den_net.parameters()) \
            + list(self.rgb_net.parameters()) \
            # + list(self.pose_cor_emb.parameters()) \
            # + list(self.frm_emb.parameters()) \
        
        # self.params = list(self.rgb_net.parameters()) \
        # self.params = list(self.pose_cor_emb.parameters())
        
        # self.ema = ExponentialMovingAverage(self.params, decay=0.995)
        # self.ce_loss = nn.CrossEntropyLoss()
        self.epoch_num = 0

        # store the non-zero voxels
        self.register_buffer('box_min_off', box_min_off.float().to(self.device))
        self.register_buffer('box_dim', box_dim.float().to(self.device))
        self.voxel_size = voxel_size
        self.max_hits = max_hits
        voxel_base_xyz = voxel_base_xyz*self.voxel_size + self.box_min_off + self.voxel_size*0.5

        self.register_buffer('voxel_base_xyz', voxel_base_xyz.float().unsqueeze(0).to(self.device))
        self.resolution_level = resolution_level
        self.sc_factor = sc_factor
        self.truncation = truncation
        self.batch_idx = -1

        num_pts_per_ray = 128
        self.min_z = 0.2
        self.max_z = max_depth
        sample = torch.linspace(self.min_z, self.max_z, num_pts_per_ray).unsqueeze(0).unsqueeze(0).to(self.device) 
        self.register_buffer('sample', sample)


        # print("Voxel shape ", voxel_base_xyz.shape)

    # def on_before_zero_grad(self, *args, **kwargs):
    #     self.ema.update(self.params)

    def get_net_op(self, points, dir_pts): #, frm_idx):

        num_batch, img_sam, ray_sam, _ = points.shape
        points = points.reshape(-1, 3)
        # print("Input network ", points.shape, dir_pts.shape)
        if(torch.min(points) < 0.0 or torch.max(points) > 1.0):
            print("Sample offset min and max ", torch.min(points, dim=0),
                torch.max(points, dim=0))

        # points = torch.zeros_like(points).to(points.device)
        den_out = self.den_net(points)
        # print("Density min and max ", torch.min(den_out, dim=0),
        #     torch.max(den_out, dim=0))

        dir_norm = torch.norm(dir_pts, dim=-1)
        dir_pts = dir_pts/dir_norm.unsqueeze(-1)

        dir_inp = dir_pts.unsqueeze(-2).repeat(1,1,ray_sam,1)
        # print(dir_inp.shape)
        dir_inp = dir_inp.reshape(-1, 3)
        # dir_inp = torch.zeros_like(dir_inp).to(dir_inp.device)
        dir_enc = self.rgb_enc(dir_inp)

        # print("Input shape ",  den_out.shape, frm_idx)

        # emb_idx = frm_idx*torch.ones(den_out.shape[0]).long().to(points.device)
        # frm_emb = self.frm_emb(emb_idx)

        # rgb_inp = torch.cat((den_out, dir_enc, frm_emb), -1)
        rgb_inp = torch.cat((den_out, dir_enc), -1)
        rgb_out = self.rgb_net(rgb_inp)
        # print(den_out.shape, dir_enc.shape, rgb_inp.shape, rgb_out.shape)

        rgb_out = rgb_out.reshape(num_batch, img_sam, ray_sam, -1)
        den_out = den_out.reshape(num_batch, img_sam, ray_sam, -1)

        return den_out, rgb_out

    def sample_points(self, ray_o, ray_d, depth, rgb):

        dpth_off = depth.unsqueeze(-1) * self.sample

        pts = ray_o.unsqueeze(-2).unsqueeze(-2) + dpth_off.unsqueeze(-1) * ray_d.unsqueeze(-2)
        # pre-process to restrict data within a box of 0-1 values
        pts = (pts - self.box_min_off + 2.1*self.min_z*self.box_dim)/((1+4.2*self.min_z)*self.box_dim)
        valid_rays = depth > 0.01

        # print("Intersection input ", ray_o.shape, ray_d.shape,
        #     pts.shape, dpth_off.shape)

        return pts, dpth_off, valid_rays

    def sample_vox_occ(self, ray_o, ray_d, depth):
        # voxel_base_xyz = self.voxel_base_xyz.to(ray_o.device)
        # self.box_min_off = self.box_min_off.to(ray_o.device)
        # self.box_dim = self.box_dim.to(ray_o.device)
        # self.voxel_size = self.voxel_size.to(ray_o.device)
        # steps = (self.box_dim / self.voxel_size).floor().long() + 1
        # print("Intersection input ", ray_o.shape, ray_d.shape,
        #     self.voxel_base_xyz.shape)

        pts_idx, min_depth, max_depth = aabb_ray_intersect(
                self.voxel_size, self.max_hits, self.voxel_base_xyz, 
                ray_o.unsqueeze(1).repeat(1, ray_d.shape[1], 1), ray_d)

        # print("Intersection output ", pts_idx.shape, min_depth.shape)
        # print(pts_idx[:10], min_depth[:10])
        # min_depth[min_depth<0.001] = 1000.0
        min_depth_val, _ = torch.min(min_depth, dim=-1)
        max_depth_val, _ = torch.max(max_depth, dim=-1)
        # print("Intersection details ", )

        # invalid_depth = torch.logical_or(min_depth_val > depth, max_depth_val < depth)

        # if(torch.sum(invalid_depth) > 0):
        #     print("Num invalid depths ", torch.sum(invalid_depth), invalid_depth.shape)


        invalid_rays = min_depth_val >= 100
        valid_rays = min_depth_val < 100
        max_depth_val[invalid_rays] = self.max_z
        min_depth_val[invalid_rays] = 0.6

        # print("Min and max depth ", torch.min(min_depth_val[valid_rays]),
        #     torch.max(max_depth_val[valid_rays]))
        # print(min_depth_val[valid_rays][:10])

        num_pts_per_ray = 128 #256 #512
        sample = torch.linspace(0, 1.0, num_pts_per_ray).float().to(ray_o.device)
        sample = sample.unsqueeze(0).unsqueeze(0)

        dpth_off = min_depth_val.unsqueeze(-1)*(1 - sample) + \
            max_depth_val.unsqueeze(-1)*sample

        # print("Intersection input ", ray_o.shape, ray_d.shape,
        #     self.voxel_base_xyz.shape, dpth_off.shape)
        pts = ray_o.unsqueeze(-2).unsqueeze(-2) + dpth_off.unsqueeze(-1) * ray_d.unsqueeze(-2)
        # pre-process to restrict data within a box of 0-1 values
        pts = (pts - self.box_min_off + 0.5*self.box_dim)/(2.0*self.box_dim)
        # pts = (pts - self.box_min_off + 0.5*self.box_dim)/(2.0*self.box_dim)
        
        # print("Variable type ", pts.type(), dpth_off.type(),
        #     min_depth_val.type(), max_depth_val.type(), sample.type())

        return pts, dpth_off, valid_rays

    def calculate_loss(self, rgb_map, depth_map, tgt_rgb, tgt_dpth, z_vals, sdf):
        # rgb_loss = F.mse_loss(rgb_map, tgt_rgb)
        # depth_loss = F.mse_loss(depth_map, tgt_dpth)
        # # alpha_loss = F.mse_loss(alpha, \
        # #     depth_pred.unsqueeze(0).unsqueeze(0).repeat(1,img_sam,1))
        # # alpha_loss = self.ce_loss(alpha, 
        # #     depth_pred.unsqueeze(0).unsqueeze(0).repeat(1,img_sam,1))
        # loss = 0.0*depth_loss + rgb_loss# + alpha_loss

        # print("Shapes ", depth_map.shape, tgt_dpth.shape, z_vals.shape, sdf.shape, rgb_map.shape)

        rgb_weight = 10.0
        depth_weight = 0.0
        fs_weight = 1.0
        trunc_weight = 60.0
        trans_weight = 10.0

        img_loss = losses.compute_loss(rgb_map, tgt_rgb)
        loss = rgb_weight * img_loss
        # Depth loss
        depth_loss = losses.get_depth_loss(depth_map, tgt_dpth)
        loss += depth_weight * depth_loss

        # Loss for free space / truncation samples
        truncation = self.truncation * self.sc_factor
        tgt_dpth = tgt_dpth.unsqueeze(-1).expand(-1, z_vals.shape[-1])
        fs_loss, sdf_loss = losses.get_sdf_loss(z_vals, tgt_dpth, sdf, truncation)
        loss += fs_weight * fs_loss + trunc_weight * sdf_loss

        # if feature_array is not None:
        #     reg_features = 0.1 * tf.reduce_mean(tf.square(feature_array.data))
        #     loss += reg_features

        # translation = self.pose_cor_emb.weight[:,3:]
        # reg_translation = torch.mean(torch.square(translation))
        # loss += trans_weight * reg_translation
        if(self.batch_idx % 100 == 0):
            print("Losses ", fs_loss, sdf_loss, depth_loss, img_loss, loss)

        return loss

    def process_batch(self, ray_o, ray_d, depth, rgb, idx_lst, valid_depth):

        # pts, dpth_off, valid_rays = self.sample_points(ray_o, ray_d, depth, rgb)
        pts, dpth_off, valid_rays = self.sample_vox_occ(ray_o, ray_d, depth)

        # emb_idx = frm_idx*torch.ones(ray_d.shape[1]).long().to(ray_d.device)
        # emb_idx = torch.tensor([frm_idx]).to(ray_d.device)
        # emb_idx = idx_lst.to(ray_d.device)
        # pose_cor_emb = self.pose_cor_emb(emb_idx)
        # c2w = cpose.Exp(pose_cor_emb[:, :3])
        # print("Embedding ", pose_cor_emb.shape, emb_idx.shape, c2w.shape, ray_d.shape, ray_o.shape,
        #     pts.shape)

        # Add rotation and offset embedding
        # print("matrix mul ")
        # print(c2w[:2, :3, :3])
        # print(pose_cor_emb[:2, :])
        # print(pts[:2, :5, 64])
        # print(ray_d[:2, :5])
        # print("Type ", ray_o.type(), ray_d.type(), depth.type(), c2w.type(), pts.type())
        # pts = torch.matmul(c2w[:, :3, :3].view(-1, 1, 1, 3, 3), pts.unsqueeze(-1)).squeeze(-1) + pose_cor_emb[:, 3:].view(-1, 1, 1, 3)
        # ray_d = torch.matmul(c2w[:, :3, :3].view(-1, 1, 3, 3), ray_d.unsqueeze(3)).squeeze(3) 
        # print(pts[:2, :5, 64])
        # print(ray_d[:2, :5])

        den_out, rgb_out = self.get_net_op(pts, ray_d)

        rgb_map, disp_map, acc_map, weights, depth_map = \
            vr.volume_render_radiance_field( rgb_out, den_out[..., 1],
                dpth_off, radiance_field_noise_std=1.0, white_background=False,
                sc_factor=self.sc_factor, truncation=self.truncation)


        loss = self.calculate_loss(rgb_map, depth_map[valid_depth!=0], rgb, depth[valid_depth!=0], 
            dpth_off[valid_depth!=0], den_out[..., 1][valid_depth!=0])
        return loss, rgb_map, depth_map, valid_rays

    def training_step(self, batch, batch_idx):
        ray_d = batch['ray_d']
        depth = batch['depth']
        rgb = batch['rgb']
        ray_o = batch['ray_o']
        box_min_off = batch['box_min_off']
        box_dim = batch['box_dim']
        idx_lst = batch['idx']
        valid_depth = batch['valid_depth']
        loss, _, _, _ = self.process_batch(ray_o, ray_d, depth, rgb, idx_lst, valid_depth)
        self.batch_idx = batch_idx

        tqdm_dict = {'train_loss': loss}
        outputs = {
            'loss': loss,
            'progress_bar': tqdm_dict,
            'log': tqdm_dict
        }
        return outputs['loss']

    # def training_epoch_end(self, training_step_outputs):
    #     for prediction in training_step_outputs:
    #         # do something with these
    #         print (prediction)

    #     return

    def validation_step(self, batch, batch_idx):

        # return

        ray_d_i = batch['ray_d']
        depth_i = batch['depth']
        rgb_i = batch['rgb']
        ray_o = batch['ray_o']
        box_min_off = batch['box_min_off']
        box_dim = batch['box_dim']
        idx_lst = batch['idx']
        valid_depth_i = batch['valid_depth']
        pred_rgb = torch.zeros(rgb_i.shape[1], rgb_i.shape[2]).to(rgb_i.device)
        pred_depth = torch.zeros(rgb_i.shape[1]).to(rgb_i.device)

        # Calculate masked loss
        # Check with a known dataset like Lego?

        total_loss = 0.0
        chunk_size = 5000 #10240
        with torch.no_grad():
            for idx in range(0, ray_d_i.shape[1], chunk_size):
                ray_d = ray_d_i[:, idx : idx+chunk_size, :]
                depth = depth_i[:, idx : idx+chunk_size]
                rgb = rgb_i[:, idx : idx+chunk_size, :]
                valid_depth = valid_depth_i[:, idx : idx+chunk_size]
                

                # print("Num sample ", ray_d.shape, batch['ray_d'].shape)            
                loss, rgb_map, depth_map, valid_rays = \
                    self.process_batch(ray_o, ray_d, depth, rgb, idx_lst, valid_depth)

                pred_rgb[idx : idx+chunk_size, :][valid_rays[0]] = rgb_map[0,:,:][valid_rays[0]]
                pred_depth[idx : idx+chunk_size][valid_rays[0]] = depth_map[0,:][valid_rays[0]]
                # pred_rgb[idx : idx+chunk_size, :] = rgb_map[0,:,:]
                # pred_depth[idx : idx+chunk_size] = depth_map[0,:]

                # total_loss += ray_d.shape[1]*loss
                # torch.cuda.empty_cache()
                # break

            # depth_i = depth_i.detach().cpu()
            # rgb_i = rgb_i.detach().cpu()
            tru_dep = valid_depth_i[0]

            # total_loss = self.calculate_loss(pred_rgb[tru_dep != 0], 
            #     pred_depth[tru_dep != 0], rgb_i[0][tru_dep != 0], depth_i[0][tru_dep != 0])
            total_loss = F.mse_loss(pred_rgb[tru_dep != 0], rgb_i[0][tru_dep != 0])


        depth_diff = 1.0*torch.ones(rgb_i.shape[1], 3).to(rgb_i.device)
        diff_img = torch.abs(pred_depth - depth_i[0,:]) / 4.0
        depth_diff[:, 0] = diff_img
        depth_diff[:, 1] = diff_img
        depth_diff[:, 2] = diff_img

        pred_dpth_img = 1.0*torch.ones(rgb_i.shape[1], 3).to(rgb_i.device)
        pred_dpth_img[:, 0] = pred_depth / 4.0
        pred_dpth_img[:, 1] = pred_depth / 4.0
        pred_dpth_img[:, 2] = pred_depth / 4.0

        org_dpth_img = 1.0*torch.ones(rgb_i.shape[1], 3).to(rgb_i.device)
        org_dpth_img[:, 0] = depth_i[0,:] / 4.0
        org_dpth_img[:, 1] = depth_i[0,:] / 4.0
        org_dpth_img[:, 2] = depth_i[0,:] / 4.0

        # if(self.epoch_num % 25 == 0 and batch_idx % 30 == 0):
        dump_image(pred_rgb, './out_images/rgb_' + \
            str(batch_idx)   + '.png',
            wth=int(1920/self.resolution_level), hgt=int(1440/self.resolution_level))

        dump_image(pred_dpth_img, './out_images/depth_' + \
            str(batch_idx)   + '.png',
            wth=int(1920/self.resolution_level), hgt=int(1440/self.resolution_level))
        
        # dump_image(org_dpth_img, './out_images/org_depth_' + \
        #     str(self.epoch_num) + '_' + str(batch_idx)   + '.png',
        #     wth=int(1920/self.resolution_level), hgt=int(1440/self.resolution_level))

        tqdm_dict = {'val_loss': total_loss}
        outputs = {
            'loss': total_loss,
            'progress_bar': tqdm_dict,
            'log': tqdm_dict,
            'val_loss' : total_loss,
            'pred_rgb' : pred_rgb,
            'depth' : pred_dpth_img,
        }

        self.log("val_loss", total_loss)


        return outputs

    def validation_epoch_end(self, outputs):

        # return
        # print("Output ", outputs)
        avg_loss = torch.stack([x['loss'] for x in outputs]).mean()
        tqdm_dict = {'val_loss': avg_loss}
        print("Val loss ", avg_loss)

        self.epoch_num += 1
        self.log("val_loss", avg_loss)

        return {
            'progress_bar': tqdm_dict,
            'log': {'val_loss': avg_loss},
            'val_loss': avg_loss,
            'loss': avg_loss,
        }


    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.params, lr=0.001, eps=1e-15, 
            betas=(0.9, 0.995), weight_decay=1e-6)
        # optimizer = torch.optim.Adam(self.params, lr=0.0001, eps=1e-15, 
        #     betas=(0.9, 0.995), weight_decay=1e-6)
        # optimizer = torch.optim.Adam(self.parameters(), lr=0.01)
        return optimizer


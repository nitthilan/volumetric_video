

import dataloader as dl
import numpy as np
import torch
from clib import (
    aabb_ray_intersect, triangle_ray_intersect, svo_ray_intersect,
    uniform_ray_sampling, inverse_cdf_sampling
)
from torchvision.transforms import ToPILImage



def bbox2voxels(vox_min, vox_dim, voxel_size):
    # vox_min, vox_max = bbox[:3], bbox[3:]
    steps = (vox_dim / voxel_size).floor().long() + 1
    x, y, z = [c.reshape(-1).astype('float32') for c in np.meshgrid(np.arange(steps[0]), np.arange(steps[1]), np.arange(steps[2]))]
    x, y, z = x * voxel_size + vox_min[0], y * voxel_size + vox_min[1], z * voxel_size + vox_min[2]
    
    return np.stack([x, y, z]).T.astype('float32'), steps

def dump_image(rgb, name, wth=int(1920/4), hgt=int(1440/4)):
    rgb = rgb.detach()
    rgb = rgb.reshape(hgt, wth, -1)
    rgb = torch.transpose(rgb, 0, 2)
    rgb = ToPILImage()(rgb)
    rgb.save(name)
    # save_image(rgb, 'rgb' + str(idx) + '.png')
    return

def calculate_occupancy(tr_dl, confidence_level, max_depth, voxel_size):

    dataset = tr_dl.get_full_data(0)
    box_min_off = dataset['box_min_off']
    box_dim = dataset['box_dim']
    # voxel_size = 0.1
    # _, steps = torch.from_numpy(bbox2voxels(box_min_off, box_dim, voxel_size))
    steps = (box_dim / voxel_size).floor().long() + 1

    num_voxel = steps[0]*steps[1]*steps[2]
    voxel_flag = torch.zeros((steps[0], steps[1], steps[2]))
    print("Shape ", steps, num_voxel, box_dim, box_min_off)

    for idx in range(tr_dl.total_files()): # 0,120,10): #
        dataset = tr_dl.get_full_data(idx)
        # print(dataset['ray_o'].shape, dataset['ray_d'].shape, dataset['depth'].shape)
        depth = dataset['depth']
        ray_d = dataset['ray_d']
        ray_o = dataset['ray_o']
        confidence = dataset['confidence']

        for offset in [0] :#[-1.73*voxel_size, 0 , 1.73*voxel_size]:
            depth_points = ray_o + ray_d*(depth.unsqueeze(-1) + offset)
            offset_points = ((depth_points - box_min_off)/voxel_size).floor().long()
            dir_norm = torch.norm(ray_d, dim=-1)

            offset_points = offset_points[confidence>=confidence_level]
            depth = depth[confidence>=confidence_level]

            offset_points = offset_points[depth <= max_depth+voxel_size]

            voxel_flag[offset_points[:, 0], offset_points[:, 1], offset_points[:, 2]] = 1

            # voxel_flag[off_idx] = 1
            # print(torch.max(offset_points, dim=0), offset_points.shape,
            #     torch.sum(voxel_flag), torch.sum(dir_norm), dir_norm.shape,
            #     torch.min(depth), torch.max(depth))
            print("Offset ", idx)

    voxel_idx = torch.nonzero(voxel_flag)

    print("Output index ", voxel_idx.shape, torch.min(voxel_idx, dim=0),
        torch.max(voxel_idx, dim=0))


    return voxel_idx

def validate_occupancy(tr_dl, confidence_level, scene_max_depth, voxel_size, voxel_base_xyz, max_hits):

    device = 'cuda:0'

    dataset = tr_dl.get_full_data(0)
    box_min_off = dataset['box_min_off'].to(device)
    box_dim = dataset['box_dim'].to(device)
    voxel_base_xyz = voxel_base_xyz.to(device)

    # voxel_size = 0.1
    # _, steps = torch.from_numpy(bbox2voxels(box_min_off, box_dim, voxel_size))
    steps = (box_dim / voxel_size).floor().long() + 1

    voxel_base_xyz = voxel_base_xyz*voxel_size + box_min_off + voxel_size*0.5

    for idx in range(tr_dl.total_files()): #0,120,10): #
        dataset = tr_dl.get_full_data(idx)
        # print(dataset['ray_o'].shape, dataset['ray_d'].shape, dataset['depth'].shape)
        depth = dataset['depth'].to(device)
        ray_d = dataset['ray_d'].to(device)
        ray_o = dataset['ray_o'].to(device)
        rgb = dataset['rgb'].to(device)
        confidence = dataset['confidence'].to(device)

        depth_points = ray_o + ray_d*depth.unsqueeze(-1)

        # print("Depth points ", ray_o, ray_d[:10], depth[:10], depth_points[:10])

        offset_points = ((depth_points - box_min_off)/voxel_size).floor().long()
        
        # offset_points = offset_points[confidence>=confidence_level]
        # depth = depth[confidence>=confidence_level]
        # offset_points = offset_points[depth <= max_depth+voxel_size]

        # offset_points = offset_points[confidence>=confidence_level]
        # ray_d = ray_d[confidence>=confidence_level]
        # # depth = depth[confidence>=confidence_level]

        # offset_points = offset_points[depth <= scene_max_depth+voxel_size]
        # ray_d = ray_d[depth <= scene_max_depth+voxel_size]
        # depth1 = depth[depth <= scene_max_depth+voxel_size]

        pts_idx, min_depth, max_depth = aabb_ray_intersect(
                voxel_size, max_hits, voxel_base_xyz.unsqueeze(0), 
                ray_o.unsqueeze(0).unsqueeze(0).repeat(1, ray_d.shape[0], 1), 
                # ray_o_off.unsqueeze(0),
                ray_d.unsqueeze(0))

        min_depth_val, _ = torch.min(min_depth, dim=-1)
        max_depth_val, _ = torch.max(max_depth, dim=-1)

        invalid_rays = min_depth_val >= 100
        valid_rays = min_depth_val < 100
        max_depth_val[invalid_rays] = 4.0
        min_depth_val[invalid_rays] = 0.6




        wth = 960
        hgt = 720
        min_voxel_depth = min_depth_val[0].reshape((wth, hgt)) / scene_max_depth
        min_voxel_depth[min_voxel_depth > 1.0] = 1.0
        max_voxel_depth = max_depth_val[0].reshape((wth, hgt)) / scene_max_depth
        max_voxel_depth[max_voxel_depth < 0.0] = 1.0
        rgb = rgb.reshape((wth, hgt, 3))
        depth = depth.reshape((wth, hgt))
        org_dpth_img = 1.0*torch.ones(wth, hgt, 3).to(min_voxel_depth.device)
        org_dpth_img[:, :, 0] = min_voxel_depth 
        org_dpth_img[:, :, 1] = min_voxel_depth
        org_dpth_img[:, :, 2] = min_voxel_depth #torch.abs(depth - min_voxel_depth)
        org_dpth_img[org_dpth_img>1.0] = 1.0
        dump_image(org_dpth_img, "inference/occ_"+str(idx)+".png", wth=wth, hgt=hgt)
        dump_image(rgb, "inference/rgb_"+str(idx)+".png", wth=wth, hgt=hgt)

        depth = depth.reshape(-1)

        min_depth_val = min_depth_val.squeeze()
        max_depth_val = max_depth_val.squeeze()
        min_depth_val = min_depth_val[confidence>=confidence_level]
        max_depth_val = max_depth_val[confidence>=confidence_level]
        depth = depth[confidence>=confidence_level]

        min_depth_val = min_depth_val[depth <= scene_max_depth+voxel_size]
        max_depth_val = max_depth_val[depth <= scene_max_depth+voxel_size]
        depth = depth[depth <= scene_max_depth+voxel_size]

        # depth = depth[depth <= scene_max_depth+voxel_size]
        invalid_depth = torch.logical_or(min_depth_val > depth, max_depth_val < depth)
        # print("Invalid depth ", min_depth_val[invalid_depth], depth.unsqueeze(0)[invalid_depth], 
        #     max_depth_val[invalid_depth], torch.sum(invalid_depth), invalid_depth.shape)
        print("Min and max depth ", torch.min(min_depth_val), torch.min(depth), torch.max(min_depth_val), 
        torch.max(depth), torch.sum(invalid_depth))
        # print("Invalid depth1 ", min_depth_val, depth.unsqueeze(0), 
        #     max_depth_val, torch.sum(invalid_depth), invalid_depth.shape)

    # print(torch.max(offset_points, dim=0), offset_points.shape,
    #     torch.sum(voxel_flag))

    return 



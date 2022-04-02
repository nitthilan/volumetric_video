

import dataloader as dl
import numpy as np
import torch
from clib import (
    aabb_ray_intersect, triangle_ray_intersect, svo_ray_intersect,
    uniform_ray_sampling, inverse_cdf_sampling
)



def bbox2voxels(vox_min, vox_dim, voxel_size):
    # vox_min, vox_max = bbox[:3], bbox[3:]
    steps = (vox_dim / voxel_size).floor().long() + 1
    x, y, z = [c.reshape(-1).astype('float32') for c in np.meshgrid(np.arange(steps[0]), np.arange(steps[1]), np.arange(steps[2]))]
    x, y, z = x * voxel_size + vox_min[0], y * voxel_size + vox_min[1], z * voxel_size + vox_min[2]
    
    return np.stack([x, y, z]).T.astype('float32'), steps



def calculate_occupancy(tr_dl, confidence_level, max_depth, voxel_size):

    dataset = tr_dl.get_full_data(0)
    box_min_off = dataset['box_min_off']
    box_dim = dataset['box_dim']
    # voxel_size = 0.1
    # _, steps = torch.from_numpy(bbox2voxels(box_min_off, box_dim, voxel_size))
    steps = (box_dim / voxel_size).floor().long() + 1

    num_voxel = steps[0]*steps[1]*steps[2]
    voxel_flag = torch.zeros(num_voxel)
    print("Shape ", steps, num_voxel, box_dim, box_min_off)

    x_area = steps[1]*steps[2]
    y_leng = steps[2]


    for idx in range(len(tr_dl)):
        dataset = tr_dl.get_full_data(idx)
        # print(dataset['ray_o'].shape, dataset['ray_d'].shape, dataset['depth'].shape)
        depth = dataset['depth']
        ray_d = dataset['ray_d']
        ray_o = dataset['ray_o']
        confidence = dataset['confidence']

        for offset in [0] :#[-1.73*voxel_size, 0 , 1.73*voxel_size]:
            depth_points = ray_o + ray_d*(depth.unsqueeze(-1) + offset)

            offset_points = ((depth_points - box_min_off)/voxel_size).floor().long()


            offset_points = offset_points[confidence>=confidence_level]
            depth1 = depth[confidence>=confidence_level]

            offset_points = offset_points[depth1 <= max_depth+voxel_size]

            off_idx = offset_points[:, 0]*x_area + offset_points[:, 1]*y_leng + offset_points[:, 2]

            voxel_flag[off_idx] = 1
            print(torch.max(offset_points, dim=0), offset_points.shape,
                torch.sum(voxel_flag))

    voxel_idx = torch.nonzero(voxel_flag)
    voxel_idx = voxel_idx.squeeze()
    voxel_x = voxel_idx.div(x_area, rounding_mode="floor")
    voxel_y = torch.remainder(voxel_idx, x_area).div(y_leng, rounding_mode="floor")
    voxel_z = torch.remainder(torch.remainder(voxel_idx, x_area), y_leng)

    voxel_xyz = torch.stack([voxel_x, voxel_y, voxel_z], dim=0)

    # check_x = torch.eq(torch.t(voxel_xyz)[:, 0], voxel_x)
    # check_y = torch.eq(torch.t(voxel_xyz)[:, 1], voxel_y)
    # check_z = torch.eq(torch.t(voxel_xyz)[:, 2], voxel_z)
    # print("Validate equality ", torch.sum(check_x), torch.sum(check_y),
    #     torch.sum(check_z))

    print(voxel_xyz.shape, voxel_x.shape)

    return voxel_xyz

def validate_occupancy(tr_dl, confidence_level, scene_max_depth, voxel_size, voxel_base_xyz, max_hits):

    device = 'cuda:0'

    dataset = tr_dl.get_full_data(0)
    box_min_off = dataset['box_min_off'].to(device)
    box_dim = dataset['box_dim'].to(device)

    # voxel_size = 0.1
    # _, steps = torch.from_numpy(bbox2voxels(box_min_off, box_dim, voxel_size))
    steps = (box_dim / voxel_size).floor().long() + 1

    num_voxel = steps[0]*steps[1]*steps[2]

    x_area = steps[1]*steps[2]
    y_leng = steps[2]


    voxel_base_xyz = voxel_base_xyz.to(device)
    voxel_base_xyz = torch.t(voxel_base_xyz)
    voxel_base_xyz = voxel_base_xyz*voxel_size + box_min_off + voxel_size*0.5

    for idx in range(len(tr_dl)):
        dataset = tr_dl.get_full_data(idx)
        # print(dataset['ray_o'].shape, dataset['ray_d'].shape, dataset['depth'].shape)
        depth = dataset['depth'].to(device)
        ray_d = dataset['ray_d'].to(device)
        ray_o = dataset['ray_o'].to(device)
        confidence = dataset['confidence'].to(device)

        depth_points = ray_o + ray_d*depth.unsqueeze(-1)

        ray_o_off = ray_o + ray_d*0.3*depth.unsqueeze(-1)

        offset_points = ((depth_points - box_min_off)/voxel_size).floor().long()


        offset_points = offset_points[confidence>=confidence_level]
        ray_d = ray_d[confidence>=confidence_level]
        ray_o_off = ray_o_off[confidence>=confidence_level]
        depth = depth[confidence>=confidence_level]

        offset_points = offset_points[depth <= scene_max_depth+voxel_size]
        ray_d = ray_d[depth <= scene_max_depth+voxel_size]
        ray_o_off = ray_o_off[depth <= scene_max_depth+voxel_size]
        depth = depth[depth <= scene_max_depth+voxel_size]

        off_idx = offset_points[:, 0]*x_area + offset_points[:, 1]*y_leng + offset_points[:, 2]

        pts_idx, min_depth, max_depth = aabb_ray_intersect(
                voxel_size, max_hits, voxel_base_xyz.unsqueeze(0), 
                ray_o.unsqueeze(0).unsqueeze(0).repeat(1, ray_d.shape[0], 1), 
                # ray_o_off.unsqueeze(0),
                ray_d.unsqueeze(0))

        min_depth_val, _ = torch.min(min_depth, dim=-1)
        max_depth_val, _ = torch.max(max_depth, dim=-1)

        invalid_depth = torch.logical_or(min_depth_val > depth, max_depth_val < depth)
        print("Invalid depth ", min_depth_val[invalid_depth], depth.unsqueeze(0)[invalid_depth], 
            max_depth_val[invalid_depth], torch.sum(invalid_depth), invalid_depth.shape)
        print("Invalid depth1 ", min_depth_val, depth.unsqueeze(0), 
            max_depth_val, torch.sum(invalid_depth), invalid_depth.shape)

    print(torch.max(offset_points, dim=0), offset_points.shape,
        torch.sum(voxel_flag))

    return 



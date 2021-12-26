
import os
import imageio
import logging
import torch.utils.data as data
import torchvision.transforms as transforms
from . import utils as u
import numpy as np
import cv2
from collections import OrderedDict
import torch


logger = logging.getLogger(__package__)




class Dataset(data.Dataset):
    def __init__(self, data_root, name, split, skip=1, 
        resolution_level=3, confidence_level=1, dpth_smpl_per = 0.10):
        super(Dataset, self).__init__()

        self.data_root = data_root
        self.name = name
        self.split = split
        self.dpth_smpl_per = dpth_smpl_per

        basedir = os.path.join(data_root, name)
        self.poses, self.intrinsics, self.depth_files, self.confidence_files, \
            self.img_files, self.img_idxs = \
            u.get_files_lst(basedir, skip, split)

        img = imageio.imread(self.img_files[self.img_idxs[0]]).astype(np.float32) / 255.
        H, W = img.shape[:2]
        self.W_orig = W
        self.H_orig = H
        self.intrinsics_orig = self.intrinsics
        self.confidence_level = confidence_level

        self.resolution_level = -1
        self.set_resolution_level(img, resolution_level)

    def set_resolution_level(self, img, resolution_level):
        if resolution_level != self.resolution_level:
            self.resolution_level = resolution_level
            self.W = self.W_orig // resolution_level
            self.H = self.H_orig // resolution_level
            self.intrinsics = np.copy(self.intrinsics_orig)
            self.intrinsics[:2, :3] /= resolution_level


    def __getitem__(self, idx):
        index = self.img_idxs[idx]
        img = imageio.imread(self.img_files[index]).astype(np.float32) / 255.

        # only load image at this time
        # print("Image shape ", img.shape)
        img = cv2.resize(img, (self.W, self.H), interpolation=cv2.INTER_AREA)
        # print("Image shape A ", img.shape)
        img = img.reshape((-1, 3))

        rays_o, rays_d = u.get_rays_single_image(self.H, self.W,
                                    self.intrinsics, self.poses[index])
        depth = u.get_depth_value(self.depth_files[index], 
            self.confidence_files[index], self.confidence_level, self.H, self.W)
        depth = depth.reshape((-1))

        near = depth.copy() * (1 - self.dpth_smpl_per)
        far = depth.copy() * (1 + self.dpth_smpl_per)

        ret = OrderedDict([
            ('ray_o', rays_o[depth != 0]),
            ('ray_d', rays_d[depth != 0]),
            ('near', near[depth != 0]),
            ('far', far[depth != 0]),
            ('rgb', img[depth != 0]),
            # ('msk', seg_msk[depth != 0]),
        ])
        # return torch tensors
        for k in ret:
            if ret[k] is not None:
                ret[k] = torch.from_numpy(ret[k])

        return ret

    def __len__(self):
        return len(self.img_idxs)

    def random_sample(self, N_rand, center_crop=False):
        '''
        :param N_rand: number of rays to be casted
        :return:
        '''
        if center_crop:
            half_H = self.H // 2
            half_W = self.W // 2
            quad_H = half_H // 2
            quad_W = half_W // 2

            # pixel coordinates
            u, v = np.meshgrid(np.arange(half_W-quad_W, half_W+quad_W),
                               np.arange(half_H-quad_H, half_H+quad_H))
            u = u.reshape(-1)
            v = v.reshape(-1)

            select_inds = np.random.choice(u.shape[0], size=(N_rand,), replace=False)

            # Convert back to original image
            select_inds = v[select_inds] * self.W + u[select_inds]
        else:
            # Random from one image
            select_inds = np.random.choice(self.H*self.W, size=(N_rand,), replace=False)

        rays_o = self.rays_o[select_inds, :]    # [N_rand, 3]
        rays_d = self.rays_d[select_inds, :]    # [N_rand, 3]
        depth = self.depth[select_inds]         # [N_rand, ]

        if self.img is not None:
            rgb = self.img[select_inds, :]          # [N_rand, 3]
        else:
            rgb = None

        ret = OrderedDict([
            ('ray_o', rays_o),
            ('ray_d', rays_d),
            ('depth', depth),
            ('rgb', rgb),
            ('img_name', self.img_path)
        ])
        # return torch tensors
        for k in ret:
            if isinstance(ret[k], np.ndarray):
                ret[k] = torch.from_numpy(ret[k])

        return ret


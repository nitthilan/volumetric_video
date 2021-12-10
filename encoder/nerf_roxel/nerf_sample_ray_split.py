import numpy as np
from collections import OrderedDict
import torch
import cv2
import imageio

########################################################################################################################
# ray batch sampling
########################################################################################################################
def get_rays_single_image(H, W, intrinsics, c2w):
    '''
    :param H: image height
    :param W: image width
    :param intrinsics: 4 by 4 intrinsic matrix
    :param c2w: 4 by 4 camera to world extrinsic matrix
    :return:
    '''
    u, v = np.meshgrid(np.arange(W), np.arange(H))

    u = u.reshape(-1).astype(dtype=np.float32) + 0.5    # add half pixel
    v = v.reshape(-1).astype(dtype=np.float32) + 0.5
    pixels = np.stack((u, v, np.ones_like(u)), axis=0)  # (3, H*W)

    rays_d = np.dot(np.linalg.inv(intrinsics[:3, :3]), pixels)
    rays_d = np.dot(c2w[:3, :3], rays_d)  # (3, H*W)
    rays_d = rays_d.transpose((1, 0))  # (H*W, 3)

    rays_o = c2w[:3, 3].reshape((1, 3))
    rays_o = np.tile(rays_o, (rays_d.shape[0], 1))  # (H*W, 3)

    return rays_o, rays_d

def get_depth_value(depth_path, confidence_path, confidence_level, feat_w, feat_h):
    depth = np.load(depth_path)
    confidence = cv2.imread(confidence_path)[:, :, 0]
    depth[confidence < confidence_level] = 0

    depth = cv2.resize(depth, (feat_w, feat_h), interpolation=cv2.INTER_NEAREST_EXACT)
    depth[depth < 10] = 0
    depth.reshape((-1))
    return depth

def get_normalized_image(img_path, width, height):
    
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    resnet_mean = torch.from_numpy(np.array([0.485, 0.456, 0.406], dtype=np.float32))
    resnet_std = torch.from_numpy(np.array([0.229, 0.224, 0.225], dtype=np.float32))
    mean = resnet_mean.unsqueeze(0).unsqueeze(-1).unsqueeze(-1) # batch dimension, width and height
    std = resnet_std.unsqueeze(0).unsqueeze(-1).unsqueeze(-1) # batch dimension, width and height

    norm_tensor = torch.from_numpy(img)
    # HxWxC => CxHxW and then adding a batch dimension
    norm_tensor = norm_tensor.permute(2,0,1).unsqueeze(0)
    norm_tensor = norm_tensor - mean # Make image mean zero
    norm_tensor = norm_tensor / std # Make std = 1
    return norm_tensor

class FeatRaySingleImage(object):
    def __init__(self, intrinsics, c2w, feat_h, feat_w,
        img_path=None, depth_path=None, confidence_path=None, 
        confidence_level=1, resolution_level=1):
        super().__init__()
        img = imageio.imread(img_path).astype(np.float32) / 255.
        H, W = img.shape[:2]
        self.W_orig = W
        self.H_orig = H
        self.intrinsics_orig = intrinsics
        self.c2w_mat = c2w

        self.feat_intrinsics = self.intrinsics.copy()
        intrinsics[0, :3] /= (self.W/feat_w)
        intrinsics[1, :3] /= (self.H/feat_h)
        # print("Intrinsincs matrix ", intrinsics, self.intrinsics, feat_w, feat_h)
        self.feat_rays_o, self.feat_rays_d = \
            get_rays_single_image(feat_h, feat_w, intrinsics, self.c2w_mat)
        self.feat_depth = get_depth_value(depth_path, confidence_path, 
            confidence_level, feat_w, feat_h)


        self.resolution_level = resolution_level
        self.W = self.W_orig // resolution_level
        self.H = self.H_orig // resolution_level
        # Make sure that the input is BRG (pre-processing has been converted from RGB to BRG)
        self.norm_img = get_normalized_image(img, self.W, self.H)

    def get_feat_rays(self):
        ret = OrderedDict([
            ('ray_o', self.feat_rays_o),
            ('ray_d', self.feat_rays_d),
            ('depth', self.feat_depth),
        ])
        # return torch tensors
        for k in ret:
            if ret[k] is not None:
                ret[k] = torch.from_numpy(ret[k])
        return ret

    def get_img(self):
        return self.norm_img



class RaySamplerSingleImage(object):
    def __init__(self,intrinsics, c2w, img_path=None, resolution_level=1, 
        confidence_level=1,depth_path=None, confidence_path=None):
        super().__init__()

        img = imageio.imread(img_path).astype(np.float32) / 255.
        H, W = img.shape[:2]
        self.W_orig = W
        self.H_orig = H
        self.intrinsics_orig = intrinsics
        self.c2w_mat = c2w

        self.img_path = img_path
        self.depth_path = depth_path
        self.confidence_path = confidence_path

        self.resolution_level = -1
        self.set_resolution_level(img, resolution_level, confidence_level)

    def set_resolution_level(self, img, resolution_level, confidence_level):
        if resolution_level != self.resolution_level:
            self.resolution_level = resolution_level
            self.W = self.W_orig // resolution_level
            self.H = self.H_orig // resolution_level
            self.intrinsics = np.copy(self.intrinsics_orig)
            self.intrinsics[:2, :3] /= resolution_level
            # only load image at this time
            self.img = cv2.resize(img, (self.W, self.H), interpolation=cv2.INTER_AREA)
            self.img = self.img.reshape((-1, 3))

            self.rays_o, self.rays_d = get_rays_single_image(self.H, self.W,
                                        self.intrinsics, self.c2w_mat)
            self.depth = get_depth_value(self.depth_path, self.confidence_path, 
                                        confidence_level, self.W, self.H)

    def get_all(self):
        ret = OrderedDict([
            ('ray_o', self.rays_o),
            ('ray_d', self.rays_d),
            ('depth', self.depth),
            ('rgb', self.img),
        ])
        # return torch tensors
        for k in ret:
            if ret[k] is not None:
                ret[k] = torch.from_numpy(ret[k])
        return ret

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

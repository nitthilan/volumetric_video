import os
import numpy as np
from collections import OrderedDict
import torch
import imageio
import torch.utils.data as data
import torchvision.transforms as transforms
from . import utils as u



class Dataset(data.Dataset):
    def __init__(self, data_root, name, split, skip=1, 
        resolution_level=1, confidence_level=1, transform=None):
        super(Dataset, self).__init__()

        self.data_root = data_root
        self.name = name
        self.split = split

        basedir = os.path.join(data_root, name)
        self.poses, self.intrinsics, self.depth_files, self.confidence_files, \
            self.img_files, self.img_idxs = \
            u.get_files_lst(basedir, skip, split)

        self.feat_h = 45 #int(1440/4) #feat_h
        self.feat_w = 60 #int(1920/4) #feat_w
        self.confidence_level = 1
        self.resolution_level = resolution_level
        # self.transform = transforms.Compose([
        #     transforms.Resize(target_image_size),
        #     transforms.ToTensor(),
        #     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        # ])
        img = imageio.imread(self.img_files[self.img_idxs[0]]).astype(np.float32) / 255.
        H, W = img.shape[:2]

        feat_intrinsics = self.intrinsics.copy()
        feat_intrinsics[0, :3] /= (W/self.feat_w)
        feat_intrinsics[1, :3] /= (H/self.feat_h)
        self.feat_intrinsics = feat_intrinsics

    def __getitem__(self, idx):
        index = self.img_idxs[idx]

        img = imageio.imread(self.img_files[index]).astype(np.float32) / 255.
        H, W = img.shape[:2]
        c2w_mat = self.poses[index]

        # print("Intrinsincs matrix ", intrinsics, self.intrinsics, feat_w, feat_h)
        feat_rays_o, feat_rays_d = \
            u.get_rays_single_image(self.feat_h, self.feat_w, self.feat_intrinsics, 
                c2w_mat)
        feat_depth, seg_msk = u.get_depth_value(self.depth_files[index], 
            self.confidence_files[index], 
            self.confidence_level, self.feat_h, self.feat_w)


        ret = OrderedDict([
            ('ray_o', feat_rays_o),
            ('ray_d', feat_rays_d),
            ('depth', feat_depth.astype(float)),
        ])
        # return torch tensors
        for k in ret:
            if ret[k] is not None:
                ret[k] = torch.from_numpy(ret[k])

        W = W // self.resolution_level
        H = H // self.resolution_level
        # Make sure that the input is BRG (pre-processing has been converted from RGB to BRG)
        norm_img = u.get_normalized_image(img, W, H)
        ret['image'] = norm_img

        return ret

    def get_cam_bbox(self):
        transl = self.poses[:, :3, 3]
        # print("Min and max dimensions ", np.min(transl, axis=0), 
        #     np.max(transl, axis=0))
        bbox_min = np.min(transl, axis=0)
        bbox_max = np.max(transl, axis=0)
        return bbox_min, bbox_max


    def __len__(self):
        # print("Total number of images ", len(self.img_idxs))
        return len(self.img_idxs)


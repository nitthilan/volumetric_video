import os
import numpy as np
from collections import OrderedDict
import torch
import imageio
import torch.utils.data as data
import torchvision.transforms as transforms
from . import utils as u
import open3d as o3d


def point_clouds(flags, data):
    """
    Converts depth maps to point clouds and merges them all into one global point cloud.
    flags: command line arguments
    data: dict with keys ['intrinsics', 'poses']
    returns: [open3d.geometry.PointCloud]
    """
    intrinsics = get_intrinsics(data['intrinsics'])
    pc = o3d.geometry.PointCloud()
    meshes = []
    for i, T_WC in enumerate(data['poses']):
        if i % flags.every != 0:
            continue
        print(f"Point cloud {i}", end="\r")
        T_CW = np.linalg.inv(T_WC)
        confidence = load_confidence(os.path.join(flags.path, 'confidence', f'{i:06}.png'))
        depth = load_depth(os.path.join(flags.path, 'depth', f'{i:06}.npy'), confidence, filter_level=flags.confidence)
        pc += o3d.geometry.PointCloud.create_from_depth_image(depth, intrinsics, extrinsic=T_CW, depth_scale=1.0)
    return [pc]

class Dataset(data.Dataset):
    def __init__(self, data_root, name, split, skip=2, 
        resolution_level=1, confidence_level=2, transform=None):
        super(Dataset, self).__init__()

        self.data_root = data_root
        self.name = name
        self.split = split

        basedir = os.path.join(data_root, name)
        self.poses, self.intrinsics, self.depth_files, self.confidence_files, \
            self.img_files, self.img_idxs = \
            u.get_files_lst(basedir, skip, split)

        self.feat_h = 180 # 45 #int(1440/4) #feat_h
        self.feat_w = 240 # 60 #int(1920/4) #feat_w
        self.confidence_level = confidence_level
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
        w2c = self.poses[index]

        # print("Intrinsincs matrix ", intrinsics, self.intrinsics, feat_w, feat_h)
        feat_rays_o, feat_rays_d = \
            u.get_rays_single_image(self.feat_h, self.feat_w, self.feat_intrinsics, 
                w2c)
        depth_img = u.get_depth_value(self.depth_files[index], 
            self.confidence_files[index], 
            self.confidence_level, self.feat_h, self.feat_w)
        feat_depth = depth_img.reshape((-1))



        # o3d_intrinsic = o3d.camera.PinholeCameraIntrinsic(
        #     width=240, height=180, 
        #     fx=self.feat_intrinsics[0, 0], fy=self.feat_intrinsics[1, 1], 
        #     cx=self.feat_intrinsics[0, 2], cy=self.feat_intrinsics[1, 2])

        # c2w = np.linalg.inv(w2c)
        # pc = o3d.geometry.PointCloud.create_from_depth_image(
        #     o3d.geometry.Image(depth_img.astype(np.float32) / 1000.0), 
        #     o3d_intrinsic, extrinsic=c2w, depth_scale=1.0)
        # pc_points = np.asarray(pc.points)

        # img_idx = (feat_depth !=0)
        # point_cloud = feat_rays_o[img_idx] + \
        #     feat_rays_d[img_idx]*np.expand_dims(feat_depth.astype(float)[img_idx], axis=-1)

        # print("Point cloud ", pc_points.shape, #pc_points[:10], 
        #     point_cloud.shape)
        # print("Point cloud ", pc_points[:10], point_cloud[:10])

        # print("Check close ", np.sum(np.abs(pc_points - point_cloud)) )


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
        depth_img = u.get_depth_value(self.depth_files[index], 
            self.confidence_files[index], 
            self.confidence_level, H, W)
        # Make sure that the input is BRG (pre-processing has been converted from RGB to BRG)
        norm_img = u.get_normalized_image(img, W, H)
        norm_img[:, depth_img <= 0.00001] = 0
        # print("Input image and depth shape ", depth_img.shape, norm_img.shape)
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


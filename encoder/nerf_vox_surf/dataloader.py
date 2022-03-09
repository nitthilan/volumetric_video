import glob
import logging
import numpy as np
import os
import random
import torch
import torch.utils.data
import json
from torchvision import transforms
from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
import pickle
from collections import OrderedDict
import cv2
import imageio
from scipy.spatial.transform import Rotation
from numpy import linalg as LA

########################################################################################################################
# ray batch sampling
########################################################################################################################
def get_rays_single_image(W, H, intrinsics, c2w):
    '''
    :param H: image height
    :param W: image width
    :param intrinsics: 4 by 4 intrinsic matrix
    :param c2w: 4 by 4 camera to world extrinsic matrix
    :return:
    '''
    u, v = np.meshgrid(np.arange(W), np.arange(H))
    # print("U and V shape ", u.shape, v.shape)

    u = u.reshape(-1).astype(dtype=np.float32) + 0.5    # add half pixel
    v = v.reshape(-1).astype(dtype=np.float32) + 0.5
    pixels = np.stack((u, v, np.ones_like(u)), axis=0)  # (3, H*W)


    rays_d = np.dot(np.linalg.inv(intrinsics[:3, :3]), pixels) # (H*W, 3)
    rays_d = rays_d.transpose((1, 0))  # (3, H*W)
    rays_d = np.dot(rays_d, c2w[:3, :3].T)
    norm_d = np.expand_dims(LA.norm(rays_d, axis=-1), axis=-1)
    rays_d = rays_d / norm_d 
    # print("mesh grid ver ", np.max(rays_d, axis=0), np.min(rays_d, axis=0), 
    #     intrinsics)
    # print(c2w[:3, 3])
    # print(rays_d.shape, LA.norm(rays_d, axis=-1)[:10])

    rays_o = c2w[:3, 3] #.reshape((1, 3))
    # rays_o = np.tile(rays_o, (rays_d.shape[0], 1))  # (H*W, 3)

    return rays_o, rays_d

def get_depth_value(depth_path, confidence_path, confidence_level, feat_w, feat_h):
    depth = np.load(depth_path)
    confidence = cv2.imread(confidence_path)[:, :, 0]


    # print("Depth and confidence ", depth.shape, confidence.shape,
    #     np.min(depth), np.max(depth), np.min(confidence), np.max(confidence))

    # print("Confidence values", np.sum(confidence==0), np.sum(confidence==1),
    #     np.sum(confidence==2))

    # print("Min Max depth Conf 0 ", np.min(depth[confidence == 0] ),
    #     np.max(depth[confidence == 0] ), np.mean(depth[confidence == 0]),
    #     depth[confidence == 0].shape)
    # print("Min Max depth Conf 1 ", np.min(depth[confidence == 1] ),
    #     np.max(depth[confidence == 1] ), np.mean(depth[confidence == 1]),
    #     depth[confidence == 1].shape)
    # print("Min Max depth Conf 2 ", np.min(depth[confidence == 2] ),
    #     np.max(depth[confidence == 2] ), np.mean(depth[confidence == 2]),
    #     depth[confidence == 2].shape)


    depth[confidence < confidence_level] = 0

    depth = cv2.resize(depth, (feat_w, feat_h), interpolation=cv2.INTER_NEAREST_EXACT)
    depth[depth < 10] = 0
    depth = depth.reshape((-1)).astype(np.float32)/1000.0
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



########################################################################################################################
# camera coordinate system: x-->right, y-->down, z-->scene (opencv/colmap convention)
# poses is camera-to-world
########################################################################################################################
def find_files(dir, exts):
    if os.path.isdir(dir):
        # types should be ['*.png', '*.jpg']
        files_grabbed = []
        for ext in exts:
            files_grabbed.extend(glob.glob(os.path.join(dir, ext)))
        if len(files_grabbed) > 0:
            files_grabbed = sorted(files_grabbed)
        return files_grabbed
    else:
        return []


def read_lines(basedir, poses):
    with open(os.path.join(basedir, 'non_blurry.txt'), 'r') as file:
        file_lst = file.read().replace('\n', ' ').split(' ')

    full_file_name = []
    depth_files = []
    confidence_files = []
    pose_list = []

    for file in sorted(file_lst)[1:]:
        full_file_name.append(os.path.join(basedir, "rgb", file))
        depth_files.append(os.path.join(basedir, "depth", file[:-4]+".npy"))
        confidence_files.append(os.path.join(basedir, "confidence", file[:-4]+".png"))
        pose_list.append(poses[int(file[:-4])])
    return full_file_name, depth_files, confidence_files, np.array(pose_list)



def read_camera_data(basedir):
    intrinsics = np.loadtxt(os.path.join(basedir, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(basedir, 'odometry.csv'), delimiter=',', skiprows=1)
    poses = []

    for line in odometry:
        # x, y, z, qx, qy, qz, qw
        # print("Line ", line)
        position = line[2:5]
        quaternion = line[5:]
        T_WC = np.eye(4)
        # print("quaternion ", quaternion, line)
        T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
        T_WC[:3, 3] = position
        poses.append(T_WC)
    return poses, intrinsics


def get_split_index(max_img_idx, split):
    skip_every = 6
    test_idx = 0
    val_idx = 1
    idx_lst = []
    for i in range(max_img_idx):
        if(split == "test" and (i%skip_every == test_idx)):
            idx_lst.append(i)
        elif(split == "val" and (i%skip_every == val_idx)):
            idx_lst.append(i)
        elif(split == "train" and (i%skip_every != test_idx) and (i%skip_every != val_idx)):
            idx_lst.append(i)

    return idx_lst

def get_files_lst(basedir, skip, split):
    if basedir[-1] == '/':          # remove trailing '/'
        basedir = basedir[:-1]

    # camera pose and intrinsics
    poses, intrinsics = read_camera_data(basedir)
    # depth and confidence files
    # depth_folder = os.path.join(basedir, "depth")
    # confidence_folder = os.path.join(basedir, "confidence")
    # depth_files = find_files(depth_folder, exts=['*.npy'])
    # confidence_files = find_files(confidence_folder, exts=['*.png'])

    # rgb image files
    # rgb_folder = os.path.join(basedir, "rgb")
    # img_files = find_files(rgb_folder, exts=['*.png', '*.jpg'])
    # print(img_files)
    img_files, depth_files, confidence_files, poses \
        = read_lines(basedir, poses)
    # print(img_files[:4], depth_files[:4], confidence_files[:4], poses[:4])


    img_files = img_files[::skip]
    depth_files = depth_files[::skip]
    confidence_files = confidence_files[::skip]
    poses = poses[::skip]
    img_cnt = len(depth_files)

    img_idxs = get_split_index(img_cnt, split)
    return poses, intrinsics, depth_files, confidence_files, img_files, img_idxs
 

def get_camera_frustum(img_size, K, W2C, frustum_length=0.5, color=[0., 1., 0.]):
    W, H = img_size
    hfov = np.rad2deg(np.arctan(W / 2. / K[0, 0]) * 2.)
    vfov = np.rad2deg(np.arctan(H / 2. / K[1, 1]) * 2.)
    half_w = frustum_length * np.tan(np.deg2rad(hfov / 2.))
    half_h = frustum_length * np.tan(np.deg2rad(vfov / 2.))

    # build view frustum for camera (I, 0)
    frustum_points = np.array([[0., 0., 0.],                          # frustum origin
                               [-half_w, -half_h, frustum_length],    # top-left image corner
                               [half_w, -half_h, frustum_length],     # top-right image corner
                               [half_w, half_h, frustum_length],      # bottom-right image corner
                               [-half_w, half_h, frustum_length]])    # bottom-left image corner
    frustum_lines = np.array([[0, i] for i in range(1, 5)] + [[i, (i+1)] for i in range(1, 4)] + [[4, 1]])
    frustum_colors = np.tile(np.array(color).reshape((1, 3)), (frustum_lines.shape[0], 1))

    # frustum_colors = np.vstack((np.tile(np.array([[1., 0., 0.]]), (4, 1)),
    #                            np.tile(np.array([[0., 1., 0.]]), (4, 1))))

    # transform view frustum from (I, 0) to (R, t)
    # C2W = np.linalg.inv(W2C)
    C2W = W2C
    # print("Frustrum points ")
    # print(frustum_points)
    frustum_points = np.dot(np.hstack((frustum_points, np.ones_like(frustum_points[:, 0:1]))), C2W.T)
    # print(frustum_points)
    frustum_points = frustum_points[:, :3] / frustum_points[:, 3:4]

    return frustum_points, frustum_lines, frustum_colors


def get_bounding_box(poses, intrinsics, depth):
    W, H = 1920, 1440
    frustum_length = 1.0
    half_w = W/2.0
    half_h = H/2.0
    frustum_points = np.array([                          # frustum origin
           [-half_w, -half_h, frustum_length],    # top-left image corner
           [half_w, -half_h, frustum_length],     # top-right image corner
           [half_w, half_h, frustum_length],      # bottom-right image corner
           [-half_w, half_h, frustum_length]])    # bottom-left image corner

    fur_pts = np.empty(shape=[0, 3])
    for c2w in poses:
        rays_d = np.dot(frustum_points, np.linalg.inv(intrinsics[:3, :3]).T) # (H*W, 3)
        rays_d = np.dot(rays_d, c2w[:3, :3].T)
        norm_d = np.expand_dims(LA.norm(rays_d, axis=-1), axis=-1)

        # print(norm_d, rays_d)
        rays_d = rays_d / norm_d 

        rays_o = c2w[:3, 3]

        frustrum_points = rays_o + depth*rays_d

        fur_pts = np.append(fur_pts, frustrum_points, axis=0)
        fur_pts = np.append(fur_pts, [rays_o], axis=0)
        # print(frustrum_points, rays_o, fur_pts.shape)

    box_min_pts = np.min(fur_pts, axis=0)
    box_max_pts = np.max(fur_pts, axis=0)
    box_dim = box_max_pts - box_min_pts
    print('Min max frustrum points ', np.min(fur_pts, axis=0),
        np.max(fur_pts, axis=0), box_dim)
    return box_min_pts, box_dim


class NVSD(torch.utils.data.Dataset):
    def __init__(self, basedir, skip, split,
        resolution_level=1, confidence_level=1, num_train_sample=10000):

        super().__init__()

        c2w, intrinsics, depth_files, confidence_files, img_files, img_idxs = \
                get_files_lst(basedir, skip, split=split)
        self.basedir = basedir
        self.skip = skip
        self.depth_files = depth_files
        self.confidence_files = confidence_files
        self.img_files = img_files
        self.c2w_mat = c2w

        self.img_idxs = img_idxs

        # Read a dummy img to get width and height
        img = imageio.imread(self.img_files[0]).astype(np.float32) / 255.
        H, W = img.shape[:2]
        self.W_orig = W
        self.H_orig = H
        self.intrinsics_orig = intrinsics

        self.resolution_level = resolution_level
        self.W = self.W_orig // resolution_level
        self.H = self.H_orig // resolution_level
        self.intrinsics = np.copy(self.intrinsics_orig)
        self.intrinsics[:2, :3] /= resolution_level
        self.confidence_level = confidence_level
        self.num_train_sample = num_train_sample

        # hardcoding for water pump
        self.max_depth = 4.0

        self.box_min_off, self.box_dim = \
            get_bounding_box(c2w, intrinsics, depth=self.max_depth)

        return

    def __len__(self):
        total_len = len(self.img_idxs)
        print("Total length ", total_len)
        return total_len 

    def __getitem__(self, idx):
        file_idx = self.img_idxs[idx]
        img = imageio.imread(self.img_files[file_idx]).astype(np.float32) / 255.
        # only load image at this time
        img = cv2.resize(img, (self.W, self.H), interpolation=cv2.INTER_AREA)
        img = img.reshape((-1, 3))

        rays_o, rays_d = get_rays_single_image(self.W, self.H,
                                    self.intrinsics, self.c2w_mat[file_idx])
        depth = get_depth_value(self.depth_files[file_idx], 
            self.confidence_files[file_idx], self.confidence_level, self.W, self.H)

        # Hardcoding for water pump
        depth[depth > self.max_depth] = 0


        img = img[depth != 0]
        rays_d = rays_d[depth != 0]
        depth = depth[depth != 0]
        # print("Num pixels ", depth.shape, rays_o.shape, rays_d.shape, img.shape )

        ret = OrderedDict([
            ('ray_o', rays_o),
            ('ray_d', rays_d),
            ('depth', depth),
            ('rgb', img),
            ('box_dim', self.box_dim),
            ('box_min_off', self.box_min_off),
        ])
        # return torch tensors
        for k in ret:
            if ret[k] is not None:
                # print(k)
                ret[k] = torch.from_numpy(ret[k])
        return ret


class NVSDM(pl.LightningDataModule):

    def __init__(self, basedir, skip=1, resolution_level=1, confidence_level=1,
        batch_size=1, num_workers=4):

        super().__init__()

        self.basedir = basedir
        self.skip = skip
        self.resolution_level = resolution_level
        self.confidence_level = confidence_level
        self.batch_size = batch_size
        self.num_workers = num_workers

    # When doing distributed training, Datamodules have two optional arguments for
    # granular control over download/prepare/splitting data:

    # OPTIONAL, called only on 1 GPU/machine
    def prepare_data(self):
        return

    # OPTIONAL, called for every GPU/machine (assigning state is OK)
    def setup(self, stage):
        return
    # return the dataloader for each split
    def train_dataloader(self):
        return DataLoader(NVSD(self.basedir, self.skip, split="train",
            resolution_level = self.resolution_level, confidence_level = self.confidence_level), 
        batch_size=self.batch_size, num_workers=self.num_workers, pin_memory=True)

    def val_dataloader(self):
        return DataLoader(NVSD(self.basedir, self.skip, split="val",
            resolution_level = self.resolution_level, confidence_level = self.confidence_level), 
        batch_size=self.batch_size, num_workers=self.num_workers, pin_memory=True)

    def test_dataloader(self):
        return DataLoader(NVSD(self.basedir, self.skip, split="test",
            resolution_level = self.resolution_level, confidence_level = self.confidence_level), 
        batch_size=self.batch_size, num_workers=self.num_workers, pin_memory=True)


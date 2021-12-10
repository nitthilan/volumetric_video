import numpy as np
import os
from scipy.spatial.transform import Rotation
import glob
import cv2
import torch

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


def read_camera_data(basedir):
    intrinsics = np.loadtxt(os.path.join(basedir, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(basedir, 'odometry.csv'), delimiter=',', skiprows=1)
    poses = []

    for line in odometry:
        # x, y, z, qx, qy, qz, qw
        position = line[2:5]
        quaternion = line[5:]
        T_WC = np.eye(4)
        # print("quaternion ", quaternion, line)
        T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
        T_WC[:3, 3] = position
        poses.append(T_WC)
    return np.array(poses), intrinsics


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
    depth_folder = os.path.join(basedir, "depth")
    confidence_folder = os.path.join(basedir, "confidence")
    depth_files = find_files(depth_folder, exts=['*.npy'])
    confidence_files = find_files(confidence_folder, exts=['*.png'])

    # rgb image files
    rgb_folder = os.path.join(basedir, "rgb")
    img_files = find_files(rgb_folder, exts=['*.png', '*.jpg'])


    img_files = img_files[::skip]
    depth_files = depth_files[::skip]
    confidence_files = confidence_files[::skip]
    poses = poses[::skip]
    img_cnt = len(depth_files)

    img_idxs = get_split_index(img_cnt, split)
    return poses, intrinsics, depth_files, confidence_files, img_files, img_idxs

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

    # print("U V ", u, v) - first width and then height

    u = u.reshape(-1).astype(dtype=np.float32) + 0.5    # add half pixel
    v = v.reshape(-1).astype(dtype=np.float32) + 0.5
    pixels = np.stack((u, v, np.ones_like(u)), axis=0)  # (3, H*W)

    rays_d = np.dot(np.linalg.inv(intrinsics[:3, :3]), pixels)
    rays_d = np.dot(c2w[:3, :3], rays_d)  # (3, H*W)
    rays_d = rays_d.transpose((1, 0))  # (H*W, 3)
    rays_d_mag = np.linalg.norm(rays_d, axis=1, keepdims=True)
    rays_d = rays_d/(rays_d_mag + 1e-7)

    rays_o = c2w[:3, 3].reshape((1, 3))
    rays_o = np.tile(rays_o, (rays_d.shape[0], 1))  # (H*W, 3)

    # print("Origin and direction ", rays_d_mag.shape, rays_d[:10], rays_d_mag[:10])

    return rays_o, rays_d

def get_depth_value(depth_path, confidence_path, confidence_level, 
    feat_h, feat_w, min_depth_th = 10, max_depth_th = 4000):
    depth = np.load(depth_path)
    confidence = cv2.imread(confidence_path)[:, :, 0]
    depth[confidence < confidence_level] = 0

    depth = cv2.resize(depth, (feat_w, feat_h), interpolation=cv2.INTER_NEAREST_EXACT)
    seg_msk = np.zeros_like(depth, dtype=float)
    # print("Depth shape ", depth.shape)
    depth[depth < min_depth_th] = 0
    seg_msk[depth < min_depth_th] = 0
    # Creating segmentation mask
    seg_msk[depth >= max_depth_th] = 0
    depth[depth >= max_depth_th] = 0
    depth = depth.reshape((-1)).astype(np.float32) / 1000.0
    seg_msk = seg_msk.reshape((-1))

    return depth, seg_msk

def get_normalized_image(img, width, height):
    
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    resnet_mean = torch.from_numpy(np.array([0.485, 0.456, 0.406], dtype=np.float32))
    resnet_std = torch.from_numpy(np.array([0.229, 0.224, 0.225], dtype=np.float32))
    mean = resnet_mean.unsqueeze(-1).unsqueeze(-1) # batch dimension, width and height
    std = resnet_std.unsqueeze(-1).unsqueeze(-1) # batch dimension, width and height

    norm_tensor = torch.from_numpy(img)
    # HxWxC => CxHxW and then adding a batch dimension
    norm_tensor = norm_tensor.permute(2,0,1)
    norm_tensor = norm_tensor - mean # Make image mean zero
    norm_tensor = norm_tensor / std # Make std = 1
    return norm_tensor



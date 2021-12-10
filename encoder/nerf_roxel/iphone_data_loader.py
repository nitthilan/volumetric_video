import os
import numpy as np
import imageio
import logging
from nerf_sample_ray_split import RaySamplerSingleImage
import glob
from scipy.spatial.transform import Rotation

logger = logging.getLogger(__package__)

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
        position = line[:3]
        quaternion = line[3:]
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


def feat_vol_dataloader(basedir, feat_h, feat_w, split, skip=1, resolution_level=1):

    poses, intrinsics, depth_files, confidence_files, img_files, img_idxs = \
        get_files_lst(basedir, skip, split)

    feat_ray_sampl = []
    for i in img_idxs:
        feat_ray_sampl.append(FeatRaySingleImage( 
            feat_h=feat_h, feat_w=feat_w, 
            intrinsics=intrinsics, c2w=poses[i],
            img_path=img_files[i],
            depth_path=depth_files[i],
            confidence_path=confidence_files[i],
            resolution_level=1))

    logger.info('Split {}, # views: {}'.format(split, len(img_idxs)))


    return feat_ray_sampl

def vox_render_dataloader(basedir, split, skip=1, resolution_level=1):
    poses, intrinsics, depth_files, confidence_files, img_files, img_idxs = \
        get_files_lst(basedir, skip, split)

    print("The length of the sequence ", len(img_idxs))
    ray_sampl = []
    for i in img_idxs:
        ray_sampl.append(RaySamplerSingleImage( 
            intrinsics=intrinsics, c2w=poses[i],
            img_path=img_files[i],
            depth_path=depth_files[i],
            confidence_path=confidence_files[i],
            resolution_level=1))

    logger.info('Split {}, # views: {}'.format(split, len(img_idxs)))


    return ray_sampl

if __name__ == "__main__":
    max_img_idx = 100
    print(get_split_index(max_img_idx, "train"))
    print(get_split_index(max_img_idx, "val"))
    print(get_split_index(max_img_idx, "test"))

    ray_sampl = vox_render_dataloader("/nitthilan/data/iphone12_pro/ZB1/", 
        "train", skip=10)






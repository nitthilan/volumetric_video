import open3d as o3d
import json
import numpy as np
import argparse
from scipy.spatial.transform import Rotation
import os
import cv2
import matplotlib.pyplot as plt


# python3 iphone_cam_pos.py --dataset  ~/Downloads/smpl/iphone12/harsh_ipadpro12/water_pump/

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str)
    # parser.add_argument('--out', type=str)
    # parser.add_argument('--confidence', type=int, default=2)
    return parser.parse_args()

def read_lines(flags):
    with open(os.path.join(flags.dataset, 'non_blurry.txt'), 'r') as file:
        file_lst = file.read().replace('\n', ' ').split(' ')

    return file_lst

def resize_depth(depth, width, height):
    out = cv2.resize(depth, (width, height), interpolation=cv2.INTER_NEAREST_EXACT)
    out[out < 10] = 0
    return out

def dpth_seg(flags, file_list):
    basefolder = flags.dataset

    conf_th = 1
    for i, file in enumerate(file_list):
        depth_path = os.path.join(basefolder, 'depth', file[:-4]+".npy")
        color_path = os.path.join(basefolder, 'rgb', file[:-4]+".jpg")
        confi_path = os.path.join(basefolder, 'confidence', file[:-4]+".png")

        depth = np.load(depth_path)
        confidence = cv2.imread(confi_path)[:, :, 0]
        image = cv2.imread(color_path)

        depth[confidence<conf_th] = 4000
        depth[depth > 2500] = 0

        depth = resize_depth(depth, 1920, 1440)
        image[depth == 0] = 0

        plt.imshow(image)
        plt.show()
        if(i==5):
            exit()





def read_data(flags):
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    file_lst = read_lines(flags)

    # print(file_lst, odometry)

    poses = []

    # for line in odometry:
    for file in sorted(file_lst[:-1]):
        # print(file[:-4])
        line = odometry[int(file[:-4])]
        # x, y, z, qx, qy, qz, qw
        position = line[2:5]
        quaternion = line[5:]
        T_WC = np.eye(4)
        # print("quaternion ", quaternion, line)
        T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
        T_WC[:3, 3] = position
        poses.append(T_WC)
    return { 'poses': poses, 'intrinsics': intrinsics }, sorted(file_lst[:-1])

if __name__ == '__main__':
    import os

    base_dir = './'
    flags = read_args()
    camera_det, file_lst = read_data(flags)
    dpth_seg(flags, file_lst)
    

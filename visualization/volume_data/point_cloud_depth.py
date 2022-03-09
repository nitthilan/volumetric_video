import json
import numpy as np
import argparse
from scipy.spatial.transform import Rotation
from numpy import linalg as LA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2


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

def read_depth_values(flags):
    file_lst = read_lines(flags)
    depth_dir_in = os.path.join(flags.dataset, 'depth')
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    confidence_folder = os.path.join(flags.dataset, "confidence")

    W, H = 256, 192
    intrinsics[:2, :3] /= (1440/192)
    confidence_level = 1

    acc_pts_cld = np.empty(shape=[0, 3])

    for idx, file in enumerate(sorted(file_lst[:-1])[::10]):
        # if '.npy' not in file:
        #     continue
        depth = np.load(os.path.join(depth_dir_in, file[:-4]+".npy")).reshape(-1)/1000.0
        line = odometry[int(file[:-4])]
        confidence = cv2.imread(os.path.join(confidence_folder, file[:-4]+".png"))[:, :, 0].reshape(-1)

        # x, y, z, qx, qy, qz, qw
        position = line[2:5]
        quaternion = line[5:]
        T_WC = np.eye(4)
        # print("quaternion ", quaternion, line)
        T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
        T_WC[:3, 3] = position
        # print(f"Writing depth frame {file}, {depth.shape}, {T_WC}, {intrinsics}")
        rays_o, rays_d = get_rays_single_image(W, H, intrinsics, T_WC)

        depth[depth > 4.0] = 0.0
        depth[depth < 0.01] = 0.0
        depth[confidence < 1.0] = 0.0

        rays_d = rays_d[depth != 0]
        depth = depth[depth != 0]

        pts_cld = rays_o + rays_d*np.expand_dims(depth, axis=-1)
        print(file, rays_o, rays_d[0], depth[0], pts_cld[0])
        print(pts_cld.shape)
        acc_pts_cld = np.append(acc_pts_cld, pts_cld[::60,:], axis=0)

        if(idx == 40):
            break


    acc_pts_cld = np.array(acc_pts_cld)
    print("Pts cld ", acc_pts_cld.shape)
    # acc_pts_cld = acc_pts_cld[::30, :]

    fig = plt.figure()
    # ax = plt.axes(projection='3d')
    ax = fig.add_subplot(111, projection='3d')
    # ax.set_ylim3d(-1.5, 0.25)
    ax.set_ylim3d(-1.5, 2.5)
    ax.set_zlim3d(-3.5, 0.5)
    ax.set_xlim3d(-1, 3)
    ax.scatter3D(acc_pts_cld[:, 0], acc_pts_cld[:, 1], \
            acc_pts_cld[:, 2],  cmap='Greens');
    plt.show()

    exit()

    return



if __name__ == '__main__':
    import os

    base_dir = './'
    flags = read_args()
    read_depth_values(flags)

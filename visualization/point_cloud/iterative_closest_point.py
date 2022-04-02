# examples/Python/Basic/icp_registration.py

import open3d as o3d
import numpy as np
import copy
import os
import argparse
from numpy import linalg as LA
from scipy.spatial.transform import Rotation
import cv2
from torch import float32
from PIL import Image
from numpy import asarray


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


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


def get_extrinsics(odometry, file):
    line = odometry[int(file[:-4])]
    # x, y, z, qx, qy, qz, qw
    position = line[2:5]
    quaternion = line[5:]
    T_WC = np.eye(4)
    # print("quaternion ", quaternion, line)
    T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
    T_WC[:3, 3] = position
    # T_WC = np.linalg.inv(T_WC)

    print("Extrinsic ", T_WC)

    return T_WC

def get_point_cloud(file, depth_dir_in, confidence_folder, odometry, W, H, intrinsics, confidence_level):
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
        depth[confidence < confidence_level] = 0.0

        rays_d = rays_d[depth != 0]
        depth = depth[depth != 0]

        pts_cld = rays_o + rays_d*np.expand_dims(depth, axis=-1)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pts_cld)
        return pcd

def get_point_cloud_frm_rgb(basefolder, filepath, intrinsic):
    depth_path = os.path.join(basefolder, 'depth', filepath[:-4]+".npy")
    color_path = os.path.join(basefolder, 'rgb', filepath[:-4]+".jpg")
    # color_raw = o3d.io.read_image(color_path)
    width = 256
    height = 192
    # color_raw = asarray(Image.open(color_path).convert('L').resize((width,height)))
    color_raw = asarray(Image.open(color_path).resize((width,height)))
    color_raw = o3d.geometry.Image(color_raw)

    depth_raw = np.load(depth_path)
    # out[out < 10] = 0
    depth_raw = o3d.geometry.Image((depth_raw).astype(np.float32))

    source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw)
    source_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        source_rgbd_image, intrinsic)
    # o3d.visualization.draw_geometries([source_pcd])
    return source_pcd, source_rgbd_image

def registering_point_clouds(flags):
    file_lst = read_lines(flags)
    depth_dir_in = os.path.join(flags.dataset, 'depth')
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    confidence_folder = os.path.join(flags.dataset, "confidence")

    W, H = 256, 192
    intrinsics[:2, :3] /= (1440/192)
    confidence_level = 1

    acc_pts_cld = np.empty(shape=[0, 3])

    file_lst_sorted = sorted(file_lst[:-1])[::10]
    df_fl_name0 = file_lst_sorted[1]
    df_fl_name1 = file_lst_sorted[17]

    # source = get_point_cloud(df_fl_name0, depth_dir_in, confidence_folder, 
    #     odometry, W, H, intrinsics, confidence_level)
    # target = get_point_cloud(df_fl_name1, depth_dir_in, confidence_folder, 
    #     odometry, W, H, intrinsics, confidence_level)
    intrinsic_matrix = o3d.camera.PinholeCameraIntrinsic()
    intrinsic_matrix.intrinsic_matrix = intrinsics
    source, source_rgbd = get_point_cloud_frm_rgb(flags.dataset, df_fl_name0, intrinsic_matrix)
    target, target_rgbd = get_point_cloud_frm_rgb(flags.dataset, df_fl_name1, intrinsic_matrix)

    source.transform(get_extrinsics(odometry, df_fl_name0))
    target.transform(get_extrinsics(odometry, df_fl_name1))
    o3d.visualization.draw_geometries([source, target])

    # option = o3d.pipelines.odometry.OdometryOption()
    # odo_init = np.identity(4)
    # print(option)

    # [success_color_term, trans_color_term,
    # info] = o3d.pipelines.odometry.compute_rgbd_odometry(
    #     source_rgbd, target_rgbd, intrinsic_matrix, odo_init,
    #     o3d.pipelines.odometry.RGBDOdometryJacobianFromColorTerm(), option)
    # [success_hybrid_term, trans_hybrid_term,
    # info] = o3d.pipelines.odometry.compute_rgbd_odometry(
    #     source_rgbd, target_rgbd, intrinsic_matrix, odo_init,
    #     o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(), option)



    # if success_color_term:
    #     print("Using RGB-D Odometry")
    #     print(trans_color_term)
    #     source_pcd_color_term = o3d.geometry.PointCloud.create_from_rgbd_image(
    #         source_rgbd, intrinsic_matrix)
    #     source_pcd_color_term.transform(trans_color_term)
    #     o3d.visualization.draw_geometries([target, source_pcd_color_term])

    # if success_hybrid_term:
    #     print("Using Hybrid RGB-D Odometry")
    #     print(trans_hybrid_term)
    #     source_pcd_hybrid_term = o3d.geometry.PointCloud.create_from_rgbd_image(
    #         source_rgbd, intrinsic_matrix)
    #     source_pcd_hybrid_term.transform(trans_hybrid_term)
    #     o3d.visualization.draw_geometries([target, source_pcd_hybrid_term])





    threshold = 0.02
    # trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
    #                         [-0.139, 0.967, -0.215, 0.7],
    #                         [0.487, 0.255, 0.835, -1.4], 
    #                         [0.0, 0.0, 0.0, 1.0]])
    trans_init = np.asarray([[1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0],
                             [0.0, 0.0, 1.0, 0.0], 
                             [0.0, 0.0, 0.0, 1.0]])
    evaluation = o3d.pipelines.registration.evaluate_registration(source, target,
                                                        threshold, trans_init)
    print(evaluation)

    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation)
    print("")
    draw_registration_result(source, target, reg_p2p.transformation)

    print("Apply point-to-plane ICP")
    source.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    target.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    reg_p2l = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    print(reg_p2l)
    print("Transformation is:")
    print(reg_p2l.transformation)
    print("")
    draw_registration_result(source, target, reg_p2l.transformation)



if __name__ == "__main__":
    import os

    base_dir = './'
    flags = read_args()
    registering_point_clouds(flags)


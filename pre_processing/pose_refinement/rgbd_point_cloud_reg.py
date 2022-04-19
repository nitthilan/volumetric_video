# examples/Python/Basic/icp_registration.py

import open3d as o3d
import numpy as np
import copy
import os
import argparse
# from numpy import linalg as LA
from scipy.spatial.transform import Rotation
from PIL import Image
from numpy import asarray
import cv2



def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
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
    # with open(os.path.join(flags.dataset, 'non_blurry.txt'), 'r') as file:
    #     file_lst = file.read().replace('\n', ' ').split(' ')
    with open(os.path.join(flags.dataset, 'unif_sam_img.txt'), 'r') as file:
        file_lst = file.read().replace('\n', ' ').split(' ')

    return file_lst[:-1:2]
    # return file_lst#[:40]



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

    # print("Extrinsic ", T_WC)

    return T_WC


def get_intrinsics(flags):
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    # W, H = 256, 192
    intrinsics[:2, :3] /= (1440/192)
    # confidence_level = 1
    intrinsic_matrix = o3d.camera.PinholeCameraIntrinsic()
    intrinsic_matrix.intrinsic_matrix = intrinsics

    return intrinsic_matrix

def get_file_lst(flags):
    file_lst = read_lines(flags)
    file_lst_sorted = sorted(file_lst[:-1])#[::10]

    # print("file ", file_lst_sorted)

    return file_lst_sorted#[:40]



def get_point_cloud_frm_rgb(basefolder, filepath, intrinsic):
    depth_path = os.path.join(basefolder, 'depth', filepath[:-4]+".npy")
    color_path = os.path.join(basefolder, 'rgb', filepath[:-4]+".jpg")
    confidence_path = os.path.join(basefolder, 'confidence', filepath[:-4]+".png")
    # color_raw = o3d.io.read_image(color_path)
    width = 256
    height = 192
    depth_thresh = 2.0
    # color_raw = asarray(Image.open(color_path).convert('L').resize((width,height)))
    color_raw = asarray(Image.open(color_path).resize((width,height)))
    color_raw = o3d.geometry.Image(color_raw)
    # o3d.visualization.draw_geometries([color_raw])

    depth_raw = np.load(depth_path)
    # out[out < 10] = 0

    confidence = cv2.imread(confidence_path)[:, :, 0]

    depth_raw[confidence <= 1] = depth_thresh + 1
    depth_raw = o3d.geometry.Image((depth_raw).astype(np.float32))

    source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, depth_trunc=depth_thresh, convert_rgb_to_intensity=False)

    # o3d.visualization.draw_geometries([source_rgbd_image])

    source_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        source_rgbd_image, intrinsic)
    # o3d.visualization.draw_geometries([source_pcd])
    source_pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    return source_pcd, source_rgbd_image


def pose_difference(source, target, src_odo):

    threshold = 0.02
    trans_init = np.asarray([[1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0],
                             [0.0, 0.0, 1.0, 0.0], 
                             [0.0, 0.0, 0.0, 1.0]])

    # trans_init = src_odo
    evaluation = o3d.pipelines.registration.evaluate_registration(source, target,
                                                        threshold, trans_init)
    print(evaluation)

    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)
    # print("Transformation is:")
    print(reg_p2p.transformation)
    # print("")
    # draw_registration_result(source, target, reg_p2p.transformation)

    print("Apply point-to-plane ICP")
    target.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    reg_p2l = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    print(reg_p2l)
    # print("Transformation is:")
    print(reg_p2l.transformation)
    # print("")
    # draw_registration_result(source, target, reg_p2l.transformation)

    # 'correspondence_set', 'fitness', 'inlier_rmse', 'transformation'
    if(reg_p2p.fitness > reg_p2l.fitness):
        reg = reg_p2p
        print("Point")
    else:
        reg = reg_p2l
        print("Plane")
    print(reg.transformation)
    return target, reg

def rgbd_pcd_pose_est(source, target, src_odo):

    current_transformation = src_odo 
    # current_transformation = np.identity(4)
    
    # draw_registration_result(source, target, current_transformation)


    radius = 0.01
    iter = 50
    result_icp = o3d.pipelines.registration.registration_colored_icp(
            source, target, radius, current_transformation,
            o3d.pipelines.registration.TransformationEstimationForColoredICP(),
            o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                            relative_rmse=1e-6,
                                                            max_iteration=iter))
    print("Colored ", result_icp, np.asarray(source.points).shape, np.asarray(target.points).shape)
    print(result_icp.transformation)
    # draw_registration_result(source, target, result_icp.transformation)
    # print("3. Colored point cloud registration")
    # for scale in range(3):
    #     iter = max_iter[scale]
    #     radius = voxel_radius[scale]
    #     print([iter, radius, scale])

    #     print("3-1. Downsample with a voxel size %.2f" % radius)
    #     source_down = source.voxel_down_sample(radius)
    #     target_down = target.voxel_down_sample(radius)

    #     print("3-2. Estimate normal.")
    #     source_down.estimate_normals(
    #         o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
    #     target_down.estimate_normals(
    #         o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

    #     print("3-3. Applying colored point cloud registration")
    #     result_icp = o3d.pipelines.registration.registration_colored_icp(
    #         source_down, target_down, radius, current_transformation,
    #         o3d.pipelines.registration.TransformationEstimationForColoredICP(),
    #         o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
    #                                                         relative_rmse=1e-6,
    #                                                         max_iteration=iter))
    #     current_transformation = result_icp.transformation
    #     print(result_icp)
    #     print(result_icp.transformation)
    #     draw_registration_result(source_down, target_down, result_icp.transformation)

    return result_icp.transformation

def check_odometry(src_odo, tgt_odo, transform):
    src_r = src_odo[:3, :3]
    src_t = src_odo[:3, 3]
    tgt_r = tgt_odo[:3, :3]
    tgt_t = tgt_odo[:3, 3]

    trs_r = transform[:3, :3]
    trs_t = transform[:3, 3]
    print("Compare T values ", trs_t, (tgt_t - src_t), tgt_t, src_t)
    print("Compare R values ")
    print(trs_r) 
    print((tgt_r.T * src_r))
    print(tgt_r)
    print(src_r)
    return

def registering_point_clouds(flags):
    # depth_dir_in = os.path.join(flags.dataset, 'depth')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    # confidence_folder = os.path.join(flags.dataset, "confidence")
    intrinsics = get_intrinsics(flags)
    file_lst_sorted = get_file_lst(flags)


    df_fl_name0 = file_lst_sorted[0]
    target_pcd, _ = get_point_cloud_frm_rgb(flags.dataset, df_fl_name0, intrinsics)
    target_pcd.transform(get_extrinsics(odometry, df_fl_name0))
    src_odo = get_extrinsics(odometry, file_lst_sorted[0])
    poses_lst = [src_odo]
    

    for idx in range(len(file_lst_sorted)-1):
        tgt_idx = idx + 1
        source_pcd, _ = get_point_cloud_frm_rgb(flags.dataset, file_lst_sorted[tgt_idx], intrinsics)
        # source_pcd.transform(get_extrinsics(odometry, file_lst_sorted[tgt_idx]))
        # tgt_odo = get_extrinsics(odometry, file_lst_sorted[tgt_idx])

        transformation = rgbd_pcd_pose_est(source_pcd, target_pcd, src_odo)
        source_pcd.transform(transformation)
        poses_lst.append(transformation)
        # draw_registration_result(source_pcd, target_pcd, transformation)
        o3d.visualization.draw_geometries([source_pcd, target_pcd])

        # target, reg = pose_difference(source_pcd, target_pcd, src_odo)
        # draw_registration_result(source_pcd, target_pcd, reg.transformation)

        target_pcd = source_pcd
        # source_pcd.transform(reg.transformation)
    
    poses_lst = np.array(poses_lst)
    np.savez(os.path.join(flags.dataset, 'color_odometry.npz'), poses_lst)
    




if __name__ == "__main__":
    import os

    base_dir = './'
    flags = read_args()
    registering_point_clouds(flags)


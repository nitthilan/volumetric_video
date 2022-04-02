import open3d as o3d
import numpy as np
# import copy
import os
import argparse
# # from numpy import linalg as LA
from scipy.spatial.transform import Rotation
from PIL import Image
from numpy import asarray



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

    # return file_lst[:-1:2]
    return file_lst[:40]

def get_intrinsics(flags):
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    # W, H = 256, 192
    intrinsics[:2, :3] /= (1440/192)
    # confidence_level = 1
    intrinsic_matrix = o3d.camera.PinholeCameraIntrinsic()
    intrinsic_matrix.intrinsic_matrix = intrinsics
    intrinsic_matrix.width = 256
    intrinsic_matrix.height = 192
    # print("Intrinsics ", intrinsics)

    return intrinsic_matrix

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


def get_point_cloud_frm_rgb(basefolder, filepath, intrinsic):
    depth_path = os.path.join(basefolder, 'depth', filepath[:-4]+".npy")
    color_path = os.path.join(basefolder, 'rgb', filepath[:-4]+".jpg")
    # color_raw = o3d.io.read_image(color_path)
    width = 256
    height = 192
    # color_raw = asarray(Image.open(color_path).convert('L').resize((width,height)))
    color_raw = asarray(Image.open(color_path).resize((width,height)))
    color_raw = o3d.geometry.Image(color_raw)
    # o3d.visualization.draw_geometries([color_raw])

    depth_raw = np.load(depth_path)
    # out[out < 10] = 0
    depth_raw = o3d.geometry.Image((depth_raw).astype(np.float32))

    source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, depth_trunc=4.0, convert_rgb_to_intensity=False)

    # o3d.visualization.draw_geometries([source_rgbd_image])

    source_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        source_rgbd_image, intrinsic)
    # o3d.visualization.draw_geometries([source_pcd])
    source_pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    return source_pcd, source_rgbd_image

def extract_mesh(flags):
    camera_poses = np.load(os.path.join(flags.dataset, 'color_odometry.npz'))['arr_0']
    file_lst = read_lines(flags)
    intrinsic_matrix = get_intrinsics(flags)
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)

    # print(dir(camera_poses), camera_poses.files)
    print(camera_poses)


    volume = o3d.pipelines.integration.ScalableTSDFVolume(
        voxel_length=4.0 / 512.0,
        sdf_trunc=0.04,
        color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)

    for i, filepath in enumerate(file_lst):
        print(camera_poses[i], get_extrinsics(odometry, filepath))
        print("Integrate {:d}-th image into the volume.".format(i))
        _, source_rgbd_image = get_point_cloud_frm_rgb(flags.dataset, filepath, intrinsic_matrix)
        volume.integrate(
            source_rgbd_image,
            intrinsic_matrix,
            # np.linalg.inv(get_extrinsics(odometry, filepath)))
            np.linalg.inv(camera_poses[i]))
    
    mesh = volume.extract_triangle_mesh()
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])
    
    return

if __name__ == "__main__":
    import os

    base_dir = './'
    flags = read_args()
    extract_mesh(flags)
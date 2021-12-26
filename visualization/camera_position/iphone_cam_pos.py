import open3d as o3d
import json
import numpy as np
import argparse
from scipy.spatial.transform import Rotation


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

def read_data(flags):
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    file_lst = read_lines(flags)

    # print(file_lst, odometry)

    poses = []

    # for line in odometry:
    for file in file_lst[:-1]:
        print(file[:-4])
        line = odometry[int(file[:-4])]
        # x, y, z, qx, qy, qz, qw
        position = line[2:5]
        quaternion = line[5:]
        T_WC = np.eye(4)
        # print("quaternion ", quaternion, line)
        T_WC[:3, :3] = Rotation.from_quat(quaternion).as_matrix()
        T_WC[:3, 3] = position
        poses.append(T_WC)
    return { 'poses': poses, 'intrinsics': intrinsics }


def get_camera_frustum(img_size, K, W2C, frustum_length=0.5, color=[0., 1., 0.]):
    W, H = img_size
    hfov = np.rad2deg(np.arctan(W / 2. / K[0, 0]) * 2.)
    vfov = np.rad2deg(np.arctan(H / 2. / K[1, 1]) * 2.)
    half_w = frustum_length * np.tan(np.deg2rad(hfov / 2.))
    half_h = frustum_length * np.tan(np.deg2rad(vfov / 2.))

    # build view frustum for camera (I, 0)
    frustum_points = np.array([[0., 0., 0.],                          # frustum origin
                               [-half_w, -half_h, -frustum_length],    # top-left image corner
                               [half_w, -half_h, -frustum_length],     # top-right image corner
                               [half_w, half_h, -frustum_length],      # bottom-right image corner
                               [-half_w, half_h, -frustum_length]])    # bottom-left image corner
    frustum_lines = np.array([[0, i] for i in range(1, 5)] + [[i, (i+1)] for i in range(1, 4)] + [[4, 1]])
    frustum_colors = np.tile(np.array(color).reshape((1, 3)), (frustum_lines.shape[0], 1))

    # frustum_colors = np.vstack((np.tile(np.array([[1., 0., 0.]]), (4, 1)),
    #                            np.tile(np.array([[0., 1., 0.]]), (4, 1))))

    # transform view frustum from (I, 0) to (R, t)
    C2W = np.linalg.inv(W2C)
    frustum_points = np.dot(np.hstack((frustum_points, np.ones_like(frustum_points[:, 0:1]))), C2W.T)
    frustum_points = frustum_points[:, :3] / frustum_points[:, 3:4]

    return frustum_points, frustum_lines, frustum_colors


def frustums2lineset(frustums):
    N = len(frustums)
    merged_points = np.zeros((N*5, 3))      # 5 vertices per frustum
    merged_lines = np.zeros((N*8, 2))       # 8 lines per frustum
    merged_colors = np.zeros((N*8, 3))      # each line gets a color

    for i, (frustum_points, frustum_lines, frustum_colors) in enumerate(frustums):
        merged_points[i*5:(i+1)*5, :] = frustum_points
        merged_lines[i*8:(i+1)*8, :] = frustum_lines + i*5
        merged_colors[i*8:(i+1)*8, :] = frustum_colors

    lineset = o3d.geometry.LineSet()
    lineset.points = o3d.utility.Vector3dVector(merged_points)
    lineset.lines = o3d.utility.Vector2iVector(merged_lines)
    lineset.colors = o3d.utility.Vector3dVector(merged_colors)

    return lineset

def visualize_cameras(colored_camera_dicts, sphere_radius, camera_size=0.1, geometry_file=None, geometry_type='mesh'):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=sphere_radius, resolution=10)
    sphere = o3d.geometry.LineSet.create_from_triangle_mesh(sphere)
    sphere.paint_uniform_color((1, 0, 0))

    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5, origin=[0., 0., 0.])
    # things_to_draw = [sphere, coord_frame]
    things_to_draw = [coord_frame]

    idx = 0
    for color, camera_dict in colored_camera_dicts:
        idx += 1

        # print("Intrinsics ", np.linalg.inv(camera_dict['intrinsics'][:3, :3]),
        #     camera_dict['intrinsics'])

        # print(camera_dict['poses'], camera_dict['intrinsics'])
        cnt = 0
        frustums = []
        C2W_list = []
        for W2C in camera_dict['poses'][::15]:
            K = camera_dict['intrinsics'] #np.array(camera_dict[img_name]['K']).reshape((4, 4))
            # W2C = np.array(camera_dict[img_name]['W2C']).reshape((4, 4))
            C2W = np.linalg.inv(W2C)

            # print("W2C and C2W ")
            # print(C2W)
            # print(W2C)
            # img_size = camera_dict[img_name]['img_size']
            img_size = (1920, 1440)
            frustums.append(get_camera_frustum(img_size, K, W2C, frustum_length=camera_size, color=color))
            C2W_list.append(np.linalg.inv(W2C))
            cnt += 1
        cameras = frustums2lineset(frustums)
        things_to_draw.append(cameras)

        C2W_list = np.array(C2W_list)
        print("Min and max ", np.min(C2W_list, axis=0), np.max(C2W_list, axis=0))
        print("Min and max ", np.min(camera_dict['poses'][::15], axis=0), \
            np.max(camera_dict['poses'][::15], axis=0))

    if geometry_file is not None:
        if geometry_type == 'mesh':
            geometry = o3d.io.read_triangle_mesh(geometry_file)
            geometry.compute_vertex_normals()
        elif geometry_type == 'pointcloud':
            geometry = o3d.io.read_point_cloud(geometry_file)
        else:
            raise Exception('Unknown geometry_type: ', geometry_type)

        things_to_draw.append(geometry)

    o3d.visualization.draw_geometries(things_to_draw)


if __name__ == '__main__':
    import os

    base_dir = './'
    flags = read_args()
    camera_det = read_data(flags)

    sphere_radius = 1.
    # train_cam_dict = json.load(open(os.path.join(base_dir, 'train/cam_dict_norm.json')))
    # test_cam_dict = json.load(open(os.path.join(base_dir, 'test/cam_dict_norm.json')))
    # path_cam_dict = json.load(open(os.path.join(base_dir, 'camera_path/cam_dict_norm.json')))

    camera_size = 0.5#0.1
    colored_camera_dicts = [([0, 1, 0], camera_det),
                            # ([0, 0, 1], test_cam_dict),
                            # ([1, 1, 0], path_cam_dict)
                            ]

    visualize_cameras(colored_camera_dicts, sphere_radius, 
                      camera_size=camera_size, geometry_file=None, geometry_type=None)

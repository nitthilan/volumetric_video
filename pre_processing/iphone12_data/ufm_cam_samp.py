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

def get_angle(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)*180/np.pi
    return angle

def avg_dist_pos(camera_det, file_lst, num_images):

    num_pos = len(camera_det['poses'])
    poses = camera_det['poses']
    cam_pos = []
    for i in range(num_pos):
        cam_pos.append(poses[i][:3, 3])
        # print()
    cam_pos = np.array(cam_pos)
    center = np.mean(cam_pos, axis=0)
    print("Center ", center)
    sampled_vector = [cam_pos[0]]
    sampled_angle = 360.0/num_images
    sampled_cam_pos = [poses[0]]
    image_idx_lst = [file_lst[0]]

    for i, _ in enumerate(cam_pos[1:]):
        vector_1 = sampled_vector[-1] - center
        vector_2 = cam_pos[i] - center
        angle = get_angle(vector_1, vector_2)
        if(angle > sampled_angle):
            sampled_vector.append(cam_pos[i])
            sampled_cam_pos.append(poses[i])
            image_idx_lst.append(file_lst[i])
            print(file_lst[i], angle, sampled_angle)

    return sampled_cam_pos, image_idx_lst





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

def visualize_cameras(sampled_cam_pos, intrinsics, camera_size=0.1):

    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5, origin=[0., 0., 0.])
    # things_to_draw = [sphere, coord_frame]
    things_to_draw = [coord_frame]

    cnt = 0
    frustums = []
    for W2C in sampled_cam_pos:#[::10]:
        K = intrinsics #np.array(camera_dict[img_name]['K']).reshape((4, 4))

        img_size = (1920, 1440)
        frustums.append(get_camera_frustum(img_size, K, W2C, frustum_length=camera_size, color=[1,0,0]))
        cnt += 1
    cameras = frustums2lineset(frustums)
    things_to_draw.append(cameras)

    o3d.visualization.draw_geometries(things_to_draw)




def sampled_images(basepath, unif_sam_img_lst):
    unif_sam_img_file = os.path.join(basepath, "unif_sam_img.txt")

    with open(unif_sam_img_file, 'w') as f:
        for item in unif_sam_img_lst:
            f.write("%s\n" % item)
    
    return




if __name__ == '__main__':
    import os

    base_dir = './'
    flags = read_args()
    camera_det, file_lst = read_data(flags)
    sampled_cam_pos, unif_sam_img_lst = avg_dist_pos(camera_det, file_lst, 200)
    print("Total pictures ", len(unif_sam_img_lst))
    visualize_cameras(sampled_cam_pos, camera_det['intrinsics'], camera_size = .3)
    
    sampled_images(flags.dataset, unif_sam_img_lst)


# examples/Python/Basic/icp_registration.py
# http://www.open3d.org/docs/release/tutorial/pipelines/multiway_registration.html
# Other options:
# https://github.com/sxyu/rgbdrec
# https://github.com/raulmur/ORB_SLAM2
# colmap depth based sparse matrix

# from statistics import correlation
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
# import open3d.geometry.voxel_down_sample 

voxel_size = 0.02
max_correspondence_distance_coarse = voxel_size * 15
max_correspondence_distance_fine = voxel_size * 1.5


def draw_registration_result(source, target, src_odo, tgt_odo):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.transform(src_odo)
    target_temp.transform(tgt_odo)
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

    return file_lst[:-1] #:15, 15:35, 35:45, 45:55, 50:60, 60:70, 70:80, 80:90, 90:100, 100:110
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


def get_pcd_list(file_lst_sorted, dataset, intrinsics):
    # flags.dataset
    # intrinsics = get_intrinsics(flags)
    # file_lst_sorted = get_file_lst(flags)
    pcd_list = []
    for file in file_lst_sorted:
        pcd, _ = get_point_cloud_frm_rgb(dataset, file, intrinsics)
        pcd_list.append(pcd)
    return pcd_list

def pairwise_registration(source, target, init_trans):
    print("Apply point-to-plane ICP")
    source = copy.deepcopy(source)
    target = copy.deepcopy(target)
    # target.transform(tgt_odo)


    icp_fine = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_fine,
        init_trans,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    
    # radius = 0.01
    # iter = 50
    # icp_fine = o3d.pipelines.registration.registration_colored_icp(
    #         source, target, radius, init_trans,
    #         o3d.pipelines.registration.TransformationEstimationForColoredICP(),
    #         o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
    #                                                         relative_rmse=1e-6,
    #                                                         max_iteration=iter))


    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)
    return transformation_icp, information_icp, icp_fine


def register_pcd_sequence(pcd_lst, odo_lst):
    pose_graph = o3d.pipelines.registration.PoseGraph()

    src_odo = odo_lst[0] #
    base_odo = np.identity(4)
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(np.identity(4)))

    n_pcds = len(pcd_lst)
    trans_list = []
    trans_list.append(base_odo)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, source_id + 4):
            if(target_id >= n_pcds):
                continue
            # src_odo = get_extrinsics(odometry, file_lst_sorted[source_id])
            tgt_odo = odo_lst[target_id]
            init_trans = np.dot(np.linalg.inv(src_odo), tgt_odo)

            transformation_icp, information_icp, icp_fine = pairwise_registration(
                pcd_lst[target_id], pcd_lst[source_id], init_trans)

            # draw_registration_result(pcd_lst[source_id], pcd_lst[target_id], src_odo, tgt_odo)
            # draw_registration_result(pcd_lst[source_id], pcd_lst[target_id], np.identity(4), transformation_icp)
            # draw_registration_result(pcd_lst[source_id], pcd_lst[target_id], np.identity(4), init_trans)

            if target_id == source_id + 1:  # odometry case
                print("Build o3d.registration.PoseGraph ", source_id, target_id, np.asarray(icp_fine.correspondence_set).shape)
                print(icp_fine)

                # if(np.asarray(icp_fine.correspondence_set).shape[0] < 20000):
                #     uncertain = True
                # else:
                #     uncertain = False
                
                uncertain = False

                base_odo = np.dot(base_odo, transformation_icp)
                # next_src_odo = transformation_icp
                trans_list.append(base_odo)
                # trans_list.append(init_trans)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(base_odo))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(
                                                   target_id,
                                                   source_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=uncertain))
            else:  # loop closure case
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(
                                                   target_id,
                                                   source_id,
                                                   transformation_icp,
                                                   information_icp,
                                                   uncertain=True))
    return pose_graph, trans_list

def corrected_visualization(pcd_lst, trans_list, visualize=False):
    # pcd_lst = get_pcd_list(file_lst_seg, dataset, intrinsics)
    print("Transform points and display")
    pcd_combined = o3d.geometry.PointCloud()
    for point_id in range(len(pcd_lst)):
        print(trans_list[point_id])
        # pcd_lst[point_id].transform(pose_graph.nodes[point_id].pose)
        pcd_lst[point_id].transform(trans_list[point_id])
        pcd_combined += pcd_lst[point_id]
    if(visualize):
        o3d.visualization.draw_geometries(pcd_lst)

    # print("Make a combined point cloud")
    # pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)
    # o3d.io.write_point_cloud("multiway_registration.pcd", pcd_combined_down)
    # o3d.visualization.draw_geometries([pcd_combined_down])
    return pcd_combined

def get_trans_list(pose_graph):
    trans_list = []
    for node in pose_graph.nodes:
        trans_list.append(node.pose)
    
    return trans_list

def correct_tgt_matrix(base_odo, corr_trans_list):
    trans_list = []
    for idx, _ in enumerate(corr_trans_list):
        corr_odo = corr_trans_list[idx]
        trans_list.append(np.dot(base_odo, corr_odo))
        # init_trans = np.dot(np.linalg.inv(src_odo), tgt_odo)
    return trans_list

def get_odo_lst(file_lst_sorted, odometry):
    odo_lst = []
    for file in file_lst_sorted:
        odo_lst.append(get_extrinsics(odometry,file))
    return odo_lst

def optimize_pose_graph(pose_graph):
    print("Optimizing PoseGraph ...")
    option = o3d.pipelines.registration.GlobalOptimizationOption(
        max_correspondence_distance=max_correspondence_distance_fine,
        edge_prune_threshold=0.25,
        reference_node=0)
    with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
        o3d.pipelines.registration.global_optimization(
            pose_graph, o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
            o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(), option)

    return pose_graph

def full_registration(flags):

    file_lst_sorted = get_file_lst(flags)
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    intrinsics = get_intrinsics(flags)
    length = len(file_lst_sorted)
    offset = 10
    num_seg_files = 10
    combined_pcd_lst = []
    combined_odo = []
    base_odo = get_extrinsics(odometry, file_lst_sorted[0])
    for file_off in range(0, length, offset):
        file_lst_seg = file_lst_sorted[file_off:file_off+num_seg_files]
        pcd_lst = get_pcd_list(file_lst_seg, flags.dataset, intrinsics)
        odo_lst = get_odo_lst(file_lst_seg, odometry)

        # pcd_lst_seg = pcd_lst[file_off:file_off+num_seg_files]
        pose_graph, _ = register_pcd_sequence(pcd_lst, odo_lst)
        pose_graph = optimize_pose_graph(pose_graph)

        trans_list = correct_tgt_matrix(odo_lst[0], get_trans_list(pose_graph))
        pcd_combined = corrected_visualization(pcd_lst, trans_list)
        combined_pcd_lst.append(pcd_combined)
        combined_odo.append(np.dot(np.linalg.inv(base_odo), trans_list[0]))
        filename = "pcd_"+str(file_off)+".pcd"
        o3d.io.write_point_cloud(filename, pcd_combined, write_ascii=False, compressed=True, print_progress=True)
        np.save("cor_odo_"+str(file_off)+".odo", np.array(trans_list))
    
    pose_graph, _ = register_pcd_sequence(combined_pcd_lst, combined_odo)
    pose_graph = optimize_pose_graph(pose_graph)
    trans_list = correct_tgt_matrix(combined_odo[0], get_trans_list(pose_graph))
    pcd_combined = corrected_visualization(combined_pcd_lst, trans_list, visualize=True)
    # return pose_graph, pcd_lst, trans_list

def combine_pcd():
    pcd_lst = []
    odo_lst = []
    voxel_size = 0.02
    for i in range(12):
        file_off = i*10
        com_pcd = o3d.io.read_point_cloud("pcd_"+str(file_off)+".pcd")
        com_pcd = com_pcd.voxel_down_sample(voxel_size=voxel_size)
        pcd_lst.append(com_pcd)
        odo_lst.append(np.identity(4))
    pcd_lst_cpy = copy.deepcopy(pcd_lst)
    pose_graph, _ = register_pcd_sequence(pcd_lst, odo_lst)
    pose_graph = optimize_pose_graph(pose_graph)
    trans_list = get_trans_list(pose_graph) #correct_tgt_matrix(combined_odo[0], get_trans_list(pose_graph))
    pcd_combined = corrected_visualization(pcd_lst, trans_list, visualize=True)

    pcd_combined = corrected_visualization(pcd_lst_cpy, odo_lst, visualize=True)

    mod_odo_lst = []
    for i in range(12):
        file_off = i*10
        com_odo = np.load("cor_odo_"+str(file_off)+".odo.npy")
        for j in range(com_odo.shape[0]):
            mod_odo = np.dot(trans_list[i], com_odo[j])
            print("Shapes ", trans_list[i].shape, com_odo.shape, mod_odo.shape)
            mod_odo_lst.append(mod_odo)

    np.save("combined_odo", np.array(mod_odo_lst))

    return pcd_combined

def visualize_full_pcd(flags):
    file_lst_sorted = get_file_lst(flags)[::4]
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
    intrinsics = get_intrinsics(flags)
    pcd_lst = get_pcd_list(file_lst_sorted, flags.dataset, intrinsics)
    odo_lst = get_odo_lst(file_lst_sorted, odometry)

    pcd_combined = corrected_visualization(pcd_lst, odo_lst, visualize=True)

    return pcd_combined

def visualize_corrected_pcd(flags):
    file_lst_sorted = get_file_lst(flags)[::4]
    intrinsics = get_intrinsics(flags)
    pcd_lst = get_pcd_list(file_lst_sorted, flags.dataset, intrinsics)

    corr_odo_lst = np.load("pose_refine_output/combined_odo.npy")[::4]
    voxel_size = 0.02

    pcd_dwn_lst = []
    for i, pcd in enumerate(pcd_lst):
        pcd_dwn_lst.append(pcd.voxel_down_sample(voxel_size=voxel_size))


    pcd_combined = corrected_visualization(pcd_dwn_lst, corr_odo_lst, visualize=True)

    return pcd_combined


if __name__ == "__main__":
    import os

    base_dir = './'
    flags = read_args()
    # full_registration(flags)
    visualize_full_pcd(flags)
    # combine_pcd()
    visualize_corrected_pcd(flags)





import argparse
import os
import numpy as np
import json
import cv2
from skvideo import io
# from stray_visualize import DEPTH_WIDTH, DEPTH_HEIGHT, _resize_camera_matrix
from scipy.spatial.transform import Rotation


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str)
    # parser.add_argument('--out', type=str)
    parser.add_argument('--confidence', type=int, default=2)
    return parser.parse_args()

def write_frames(stray_app_path):
    rgb_video = os.path.join(stray_app_path, 'rgb.mp4')
    rgb_out_dir = os.path.join(stray_app_path, 'rgb')
    os.makedirs(rgb_out_dir, exist_ok=True)

    OUT_WIDTH = 1920
    OUT_HEIGHT = 1440

    video = io.vreader(rgb_video)
    for i, frame in enumerate(video):
        # print(f"Writing rgb frame {i:06}" + " " * 10, end='\r')
        print("Writing rgb frame ", i, frame.shape, OUT_WIDTH, OUT_HEIGHT)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if(OUT_WIDTH != frame.shape[1] or OUT_HEIGHT != frame.shape[0]):
        	frame = cv2.resize(frame, (OUT_WIDTH, OUT_HEIGHT))
        frame_path = os.path.join(rgb_out_dir, f"{i:06}.jpg")
        params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        cv2.imwrite(frame_path, frame, params)

def resize_depth(depth):
    out = cv2.resize(depth, (OUT_WIDTH, OUT_HEIGHT), interpolation=cv2.INTER_NEAREST_EXACT)
    out[out < 10] = 0
    return out

def write_depth(flags):
    depth_out_dir = os.path.join(flags.dataset, 'processed_depth') 
    os.makedirs(depth_out_dir, exist_ok=True)

    depth_dir_in = os.path.join(flags.dataset, 'depth')
    confidence_dir = os.path.join(flags.dataset, 'confidence')
    files = sorted(os.listdir(depth_dir_in))
    for filename in files:
        if '.npy' not in filename:
            continue
        print(f"Writing depth frame {filename}", end='\r')
        number, _ = filename.split('.')
        depth = np.load(os.path.join(depth_dir_in, filename))
        confidence = cv2.imread(os.path.join(confidence_dir, number + '.png'))[:, :, 0]

        print("Depth and confidence ", depth.shape, confidence.shape,
            np.min(depth), np.max(depth), np.min(confidence), np.max(confidence))

        print("Confidence values", np.sum(confidence==0), np.sum(confidence==1),
            np.sum(confidence==2))

        print("Min Max depth Conf 0 ", np.min(depth[confidence == 0] ),
            np.max(depth[confidence == 0] ), np.mean(depth[confidence == 0]),
            depth[confidence == 0].shape)
        print("Min Max depth Conf 1 ", np.min(depth[confidence == 1] ),
            np.max(depth[confidence == 1] ), np.mean(depth[confidence == 1]),
            depth[confidence == 1].shape)
        print("Min Max depth Conf 2 ", np.min(depth[confidence == 2] ),
            np.max(depth[confidence == 2] ), np.mean(depth[confidence == 2]),
            depth[confidence == 2].shape)
        # depth[confidence < flags.confidence] = 0
        # depth = resize_depth(depth)
        # cv2.imwrite(os.path.join(depth_out_dir, number + '.png'), depth)

def resize_depth(depth, width, height):
    out = cv2.resize(depth, (width, height), interpolation=cv2.INTER_NEAREST_EXACT)
    out[out < 10] = 0
    return out

def write_depth_seg_mask(flags, width, height):
    depth_out_dir = os.path.join(flags.dataset, 'depth_seg_mask') 
    os.makedirs(depth_out_dir, exist_ok=True)

    depth_dir_in = os.path.join(flags.dataset, 'depth')
    confidence_dir = os.path.join(flags.dataset, 'confidence')
    files = sorted(os.listdir(depth_dir_in))
    for filename in files:
        if '.npy' not in filename:
            continue
        print(f"Writing depth frame {filename}", end='\r')
        number, _ = filename.split('.')
        depth = np.load(os.path.join(depth_dir_in, filename))
        confidence = cv2.imread(os.path.join(confidence_dir, number + '.png'))[:, :, 0]

        file_path = os.path.join(depth_out_dir, number+".png")

        depth[confidence < flags.confidence] = 0

        depth = resize_depth(depth, width, height)
        depth[depth >= 4000] = 0
        depth[depth != 0] = 1
        print("depth image ", depth.shape, width, height, end='\r')

        # cv2.imwrite(os.path.join(depth_out_dir, number + '.png'), depth)
        # depth.dtype='uint8'
        cv2.imwrite(file_path, (depth * 255).astype(np.uint8))


def _resize_camera_matrix(camera_matrix, scale_x, scale_y):
    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    return np.array([[fx * scale_x, 0.0, cx * scale_x],
        [0., fy * scale_y, cy * scale_y],
        [0., 0., 1.0]])

def read_data(flags):
    intrinsics = np.loadtxt(os.path.join(flags.dataset, 'camera_matrix.csv'), delimiter=',')
    odometry = np.loadtxt(os.path.join(flags.dataset, 'odometry.csv'), delimiter=',', skiprows=1)
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
    return { 'poses': poses, 'intrinsics': intrinsics }



def main():
    flags = read_args()
    # write_frames(flags.dataset)
    write_depth_seg_mask(flags, 1920, 1440)
    # write_depth(flags)
    cam_info = read_data(flags)
    print(len(cam_info['poses']))


if __name__ == "__main__":
    main()

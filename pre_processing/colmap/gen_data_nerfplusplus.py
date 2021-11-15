
import os
import shutil
import json
import numpy as np

image_folder_path="/nitthilan/data/nerfplusplus/tanks_and_temples_video/Playground/images/"
camera_param_path="/nitthilan/data/nerfplusplus/tanks_and_temples_video/Playground/colmap/cameras_normalized.json"

output_basefolder="/nitthilan/data/nerfplusplus/tanks_and_temples_video/Playground/nerfpp/"

def gen_dataset(camera_param_path, image_folder_path, output_basefolder):
	
	cam_intrinsic_folder = []
	cam_pose_folder = []
	rgb_folder = []
	for datatype in ["train", "validation"]:
		print(datatype)
		datatype_folder = os.path.join(output_basefolder, datatype)
		os.makedirs(datatype_folder, exist_ok = True)
		cam_intrinsic_folder.append(os.path.join(datatype_folder, "intrinsics"))
		os.makedirs(cam_intrinsic_folder[-1], exist_ok = True)
		cam_pose_folder.append(os.path.join(datatype_folder, "pose"))
		os.makedirs(cam_pose_folder[-1], exist_ok = True)
		rgb_folder.append(os.path.join(datatype_folder, "rgb"))
		os.makedirs(rgb_folder[-1], exist_ok = True)

	# get all files
	filelist = os.listdir(image_folder_path)
	print("total files ", len(filelist))


	with open(camera_param_path) as f:
		camera_param = json.load(f)

	# Copy images
	pick_every = 30
	for i in range(len(filelist)):
		camera_param_val = camera_param[filelist[i]]
		if(i%pick_every == 0):
			out_idx = 1
		if(i%pick_every != 0):
			out_idx = 0

		shutil.copy2(os.path.join(image_folder_path, filelist[i]), 
			rgb_folder[out_idx])
		# print(camera_param_val['K'], camera_param_val['W2C'])
		np.savetxt(os.path.join(cam_intrinsic_folder[out_idx], 
			filelist[i][:-4]+".txt"), np.array(camera_param_val['K']), 
			newline=" ", fmt='%6.5f')
		C2W = np.linalg.inv(np.array(camera_param_val['W2C']).reshape((4, 4))).flatten()
		np.savetxt(os.path.join(cam_pose_folder[out_idx], 
			filelist[i][:-4]+".txt"), C2W, newline=" ", fmt='%6.5f')


	# write intrinsics and pose

	return


gen_dataset(camera_param_path, image_folder_path, output_basefolder)
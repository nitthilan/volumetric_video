
# This would generate the volumetric image feature using the images
import torch
import numpy as np
from fairnr.clib import (
    aabb_ray_intersect, triangle_ray_intersect, svo_ray_intersect,
    uniform_ray_sampling, inverse_cdf_sampling
)

def bbox2voxels(bbox, voxel_size):
	vox_min, vox_max = bbox[:3], bbox[3:]
	# print("Size ", bbox, vox_min, vox_max)

	steps = ((vox_max - vox_min) / voxel_size).round().astype('int64') + 1
	x, y, z = [c.reshape(-1).astype('float32') for c in np.meshgrid(np.arange(steps[0]), np.arange(steps[1]), np.arange(steps[2]))]
	x, y, z = x * voxel_size + vox_min[0], y * voxel_size + vox_min[1], z * voxel_size + vox_min[2]

	return torch.from_numpy(np.stack([x, y, z]).T.astype('float32'))


def inv_bbox2voxels(num_vox_per_dir, max_distance):
	# x1 = np.logspace(1.0, max_distance, num_vox_per_dir, endpoint=True)
	x_spacing = np.geomspace(1.0, max_distance, num_vox_per_dir, endpoint=True)
	x_axes = np.sort(np.append(x_spacing, -1*x_spacing))
	voxel_dim = x_axes[1:] - x_axes[:-1]
	x, y, z = [c.reshape(-1).astype('float32') for c in \
		np.meshgrid(x_axes[:-1], x_axes[:-1], x_axes[:-1])]
	vdx, vdy, vdz = [c.reshape(-1).astype('float32') for c in \
		np.meshgrid(voxel_dim, voxel_dim, voxel_dim)]

	# Convert it to voxel center

	return torch.from_numpy(np.stack([x, y, z]).T.astype('float32')),\
		torch.from_numpy(np.stack([vdx, vdy, vdz]).T.astype('float32'))


class VolImgFeat(object):
	def __init__(self, bbox, num_vox_per_dir, max_distance, feat_dim,
		max_hits):
		super().__init__()

		self.dpth_spc_vox_dim = 2.0/num_vox_per_dir
		self.max_hits = 100

		self.dpth_spc_base = bbox2voxels(bbox, self.dpth_spc_vox_dim)
		self.dpth_spc_base += (self.dpth_spc_vox_dim/2.0)

		self.inv_dpth_spc_base, self.inv_dpth_spc_dim = \
			inv_bbox2voxels(num_vox_per_dir, max_distance)

		self.dpth_spc_mean_feat = torch.zeros(self.dpth_spc_base.shape[0], \
			feat_dim, dtype=torch.float)
		self.dpth_spc_sqr_mean_feat = torch.zeros(self.dpth_spc_base.shape[0], \
			feat_dim, dtype=torch.float)
		self.dpth_spc_num_rays = torch.zeros(self.dpth_spc_base.shape[0], \
			feat_dim, dtype=torch.float)

		# self.inv_dpth_spc_mean_feat
		# self.inv_dpth_spc_sqr_mean_feat
		# self.inv_dpth_spc_num_rays

	# 
	def gen_img_feat(self):
		return

	def get_feature_volumes(self):
		return self.dpth_spc_mean_feat, self.dpth_spc_sqr_mean_feat

	def gen_sparse_feat(self):
		return

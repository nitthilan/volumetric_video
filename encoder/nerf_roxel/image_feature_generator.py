
import numpy as np
from fairnr.clib import (
    aabb_ray_intersect, triangle_ray_intersect, svo_ray_intersect,
    uniform_ray_sampling, inverse_cdf_sampling
)


def bbox2voxels(bbox, voxel_size):
    vox_min, vox_max = bbox[:3], bbox[3:]
    steps = ((vox_max - vox_min) / voxel_size).round().astype('int64') + 1
    x, y, z = [c.reshape(-1).astype('float32') for c in np.meshgrid(np.arange(steps[0]), np.arange(steps[1]), np.arange(steps[2]))]
    x, y, z = x * voxel_size + vox_min[0], y * voxel_size + vox_min[1], z * voxel_size + vox_min[2]
    
    return np.stack([x, y, z]).T.astype('float32')


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

	return np.stack([x, y, z]).T.astype('float32'), np.stack([vdx, vdy, vdz]).T.astype('float32')


def hi():
    ray_start = ray_start.expand_as(ray_dir).contiguous().view(S, V * P, 3).contiguous()
    ray_dir = ray_dir.reshape(S, V * P, 3).contiguous()

    if self.use_octree:  # ray-voxel intersection with SVO
        flatten_centers = encoder_states['voxel_octree_center_xyz']
        flatten_children = encoder_states['voxel_octree_children_idx']
        pts_idx, min_depth, max_depth = svo_ray_intersect(
            self.voxel_size, self.max_hits, flatten_centers, flatten_children,
            ray_start, ray_dir)
    else:   # ray-voxel intersection with all voxels
        pts_idx, min_depth, max_depth = aabb_ray_intersect(
            self.voxel_size, self.max_hits, point_xyz, ray_start, ray_dir)

    # sort the depths
    min_depth.masked_fill_(pts_idx.eq(-1), MAX_DEPTH)
    max_depth.masked_fill_(pts_idx.eq(-1), MAX_DEPTH)
    min_depth, sorted_idx = min_depth.sort(dim=-1)
    max_depth = max_depth.gather(-1, sorted_idx)
    pts_idx = pts_idx.gather(-1, sorted_idx)
    hits = pts_idx.ne(-1).any(-1)  # remove all points that completely miss the object



bbox = np.array([-1, -1, -1, 1, 1, 1])
num_vox_per_dir = 10
max_distance = 1000.0
voxel_size = 2.0/num_vox_per_dir

vox_vert_list = bbox2voxels(bbox, voxel_size)

print(vox_vert_list.shape, voxel_size, bbox)

print(vox_vert_list)

vox_base, vox_dim = inv_bbox2voxels(num_vox_per_dir, max_distance)
print(vox_base.shape, vox_dim.shape)


aabb_ray_intersect


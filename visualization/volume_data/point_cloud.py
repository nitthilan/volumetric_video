import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


basepath = "/Users/kannappanjayakodinitthilan/Documents/old_laptop/virtual_studio/data/output_dec13_2021/"

coord_path = os.path.join(basepath, "coord_np.npy")
coord = np.load(coord_path)

coord_high_var_path = os.path.join(basepath, "coord_high_var_np.npy")
coord_high_var = np.load(coord_high_var_path)

num_feat_path = os.path.join(basepath, "num_feat_np.npy")
num_feat = np.load(num_feat_path)

pc_path = os.path.join(basepath, "point_cloud_0.npy")
point_cloud_0 = np.load(pc_path)
pc_path = os.path.join(basepath, "point_cloud_1.npy")
point_cloud_1 = np.load(pc_path)
point_cloud = np.append(point_cloud_0, point_cloud_1, axis=0)
print(point_cloud.shape)

print(coord.shape, num_feat.shape, point_cloud.shape)

hist, bin_edges = np.histogram(num_feat)
print(hist, bin_edges)

fig = plt.figure()
# ax = plt.axes(projection='3d')
ax = fig.add_subplot(111, projection='3d')

feat_filt = 1000
coord = coord[num_feat < feat_filt]
num_feat = num_feat[num_feat < feat_filt]

ax.set_ylim3d(0, 60)
# ax.scatter3D(coord[:, 1], coord[:, 2], coord[:, 3],  cmap='Greens');
ax.scatter3D(coord_high_var[:, 1], coord_high_var[:, 2], \
	coord_high_var[:, 3],  cmap='Greens');

# ax.set_ylim3d(-1.5, 2.5)
# ax.scatter3D(point_cloud[::1000, 0], point_cloud[::1000, 1], point_cloud[::1000, 2]);

plt.show()





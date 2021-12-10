

Using LiDAR Mode: Scan objects and get texture and mesh baked into the 3D volume
Since we know the continous camera position this means more region is overlapping. Can this be used by homography to identify parts which are overlapping and parts which do not - hard since with infinite depth it would overlap fully?

Use lidar information: It is precise for around 4 meters.
Can using LIDAR, camera position and Stereo(??) can we capture and encode a human motion in 3D when it is captured from different angles?
- Use VIBE 

LIDAR can help in surface captures easily?
Point cloud to mesh - baseline
Point cloud using depth 

App for recording depth and stereo images and video from iPhone (Stereo is not a need if we have video)

KiloNerf or NSVF for ray casting and voxel interaction


Read about ADOP since it uses point cloud as input can using depth help quality better

Read about homography and spherical harmonics

Easiest solution would be point cloud and image backprojection

Algorithm:
==========

- Input image HxW dimension (Can be resized?)
- Build a Grid of dimension N^3 (Two grids for near objects in depth space and far objects in inverse depth space camera)
- Feature Extractor: 2D CNN (new or pretrained)
- Feature Mapper: 
	- Ray casting along the pixel and find the intersecting voxels (both the near and far grids)
		- NSVF (This works well) and KiloNeRF ??
	- Find the mean and variance of all the feature vector intersecting with the voxel
	- Can High variance parts be culled? Can the voxels which do not have enough number of image features projected on them be removed?
	- Create a Cost Volume
	- Since we are averaging and value we want are for the edge of voxels, move the grid by half voxel and accumulate values inside this voxel
- 3D convolution to smooth and regularize the features
	- The Cost volume is mapped to a Neural Feature volume
	- The mean could be used for color prediction and the variance to predict 
	- Use the variance to cull the 3D volume and use Sparse convolution
- For every new viewing angle, use a Nerf or a MLP to predict the opacity and Spherical harmonics 
- Use bayesian optimization to optimize the training time for the neural network
- Check whether this generalizes across different scenes since the input features are pre-trained?

# Choose a set of N images
# Create depth space and inv depth space 
# Extract Mean and Mean Squared and num rays per voxel and bool
# Try using segmentation based features instead of resnet
# Prune the space 
# create two models for depth and inv depth space
# Training loop
# Renderer
# Increase the voxel resolution
# BO idea

- Feature generator: This module takes as input a set of images from all the camera views. Outputs two feature volumes (1) Depth space volume (2) Inverse depth space volume


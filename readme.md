
## Deep Neural Radiance Field-based 3D Volumetric Video Capture, Rendering, and Streaming [Website](https://nitthilan.github.io/to_infinity_and_beyond/)



### Overview:

A user scans the 3D environment he wants to store, as a video capturing it from different viewing angles. He can use multiple cameras to capture more information about the environment like actions. We use artificial intelligence to reconstruct and encode the 3D environment using the different videos captured by the user. Unlike other methods which use laser or depth sensors to estimate point clouds, we just use the scanned RGB monocular videos to reconstruct the environment. Finally, this captured 3D environment is viewed using a VR headset in a 360-degree stereoscopic panorama. A stereoscopic photo is a pair of images, taken simultaneously with two lenses placed like our eyes, about 65 mm apart and looking in the same direction. When presented to the two eyes by a stereoscope, these images give most people the impression of seeing a 3D space. A stereoscopic panorama is a pair of 360-degree images, which when viewed with synchronized pano viewers (like a VR headset) presents a stereo pair. Further, as the user moves around in the environment, we generate the corresponding stereo pair based on the user position to give the user an immersive 3D experience

### Modules: [details]([Website](https://nitthilan.github.io/to_infinity_and_beyond/))

#### Multi-view capture system

#### Split neural encoder, renderer and compositor

#### 360 Stereo video encoder


### Folder structure:

#### Pre-processing:
- iPhone:
- Colmap - Used code from [nerf++](https://github.com/Kai-46/nerfplusplus). The input video is pre-processed by splitting into multiple images and the corresponding camera parameters are estimated. The folder has utilities that help in this estimation

#### Encoder:

- nerf-pytorch - Pytorch implementation of nerf code taken from [nerf-pytorch](https://github.com/yenchenlin/nerf-pytorch)
- nerfplusplus - Pytorch implementation of nerf code taken from [nerf++](https://github.com/Kai-46/nerfplusplus)
- nerf_roxel - Proposed voxel based nerf for capturing the whole scene


#### VR endpoint:

- stereo_photo_app - Unity application for receiving 360-degree panorama stereo photos and displaying them on a VR headset. Currently using Occulus 2



### Task list:

## Stage 2

- Check the detailed architecture for the current implementation
- Dataloader and feature extractor module based on depth - 1 day - Done
- Data generation using iPhone/iPad Pro - 0.5 day - Done
- Inverse depth space nerf++ renderer - 1 day
- Training loop for non-rigid neural renderer - 2 days - Done
	- 3D sparse convolution
	- raycasting based rendering using volumetric prediction head
	- Dataloader and cost function implementation

- Testing and Debugging (Completion of basic pipeline) - 2 days
- Experiment with surface prediction head - 2 day
- Non-rigid volume renderer - 3 days
	- Pose estimation using LiDAR
	- Volume feature generator using ray triangle intersection
	- Testing and Debugging
- Unity VR application using hand gestures and locomotion - 3 days


## Stage 1

- Individual modules are available for each module
- Implemented a end to end pipeline from capturing a video to rendering it and visualizing the output using a VR headset
- Baseline modules used: 
	- Colmap: To learn camera parameters
	- Nerf++: Encoding unbound scenes using an inverted sphere parameterization
	- Unity Oculus VR App: Rendering Stereo 360 degree panoroma images at different camera positions
- Learnings:
	- Colmap takes exponentially more time to identify camera parameters when the number of images to be registered are large. The mapper module spends 17 minutes for 200 odd images and this increases to 1-2 hours with 500 images and larger dimension
	- Training time for Nerf++ - Takes 18-24 hours on a 4 GPU system
	- Slow inference times - 14 seconds per 4000x4000 dimension image (top bottom stereo)
- Using 360 degree panoroma stereo may not work. So initially try just planar stereo like the demo videos
- End to end pipeline with best qualities picked from different NeRF/MVS implementation
- Reduce the time across the whole pipeline. Major bottlenecks:
	- Colmap based structure from motion (SfM) estimation
	- Overfitting the NeRF module with excessive input views
	- Depth estimation for feature mapping and dense voxel processing over the whole volume
- The whole pipeline is implemented in Neural radiance field based solution

## Stage 0

- The encoding (or storage) is time-consuming since it depends on the training time which is at present in the order of hours
- The streaming delay would still be significant since it is done through the cloud


Update website with the implementation details:
Current Baseline and Pitfalls
=============================
Colmap
Nerf++
Inference times
Training times
Time taken at each stage



https://www.cs.cornell.edu/~zl548/NSFF/ - Neural Scene Flow Fields for Space-Time View Synthesis of Dynamic Scenes - Storing the video in neural network

Proposed solution:
=================
An unifying architecture which combines the capabilities of NeRF and 3D convolutions??

Input dimension: 3840x2160, 1920x1440

How is my method different from the earlier methods
- Trying to uses 2D features say from ResNet so there is a prior and so can learn faster
- Bayesian optimization since inference times are faster we can estimate where there are less quality and 
- Since we are using 2D features probably this will generalize across all the outputs
- Other than this we have removed the dependency on Colmap, and depth estimation for ray intersection with voxel or SMPLX since we are using Lidar and camera paramters from iPad Pro data


----------
Distributed Communication:
https://pytorch.org/docs/stable/distributed.html
https://pytorch.org/tutorials/intermediate/dist_tuto.html
https://pytorch.org/tutorials/beginner/dist_overview.html

---------- 
- Generating features directly from 2D images:
- Using 3D convolution and nerf together
- MVSNeRF : 
- Neural Body : 3D sparse convolution
- Can features be generated for Neural body too by convolution


Generate an initial estimate of the scene using NeRF to identify the object boundaries:
Empty Space Skipping:
- Use sparsity prior in PlenOctree and try learning those regions more with higher priority
- Opacity Regularization using Cauchy loss during training: [Baking Neural Radiance Fields for Real-Time View Synthesis]

Early Ray Termination:

Can sigma value at voxel level be used as a probability distribution for sampling rays?

Would adding a neural network at the voxel level increase the quality of the output rendering at the expense of (like NSVF)?

NSVF has voxel features instead of storing color or Spherical harmonics
Can this feature be made as view-independent and view dependent features?

Can these features be learnt directly from images using CNN features and homography? - generating cnn features and 





Add camera position as an input to the feature generated to regress 



UNISURF based hybrid solution where learning surfaces for nearby objects - probably with LIDAR data this could be a better solution?

How is Neural Bodies comming into picture?

Can stereo capture in iPhone help in capturing neural bodies without multiple cameras?


Open3D based baseline using RGBD: (Lidar data):
- [StrayVisualizer](https://github.com/kekeblom/StrayVisualizer)
- [open3d tutorial](http://www.open3d.org/docs/release/tutorial/pipelines/index.html)
- https://apps.apple.com/ci/app/stray-scanner/id1557051662?l=en
- https://www.it-jim.com/blog/iphones-12-pro-lidar-how-to-get-and-interpret-data/

Correcting camera tracking and position data over time and calibration: https://tomas789.medium.com/iphone-calibration-camera-imu-and-kalibr-33b8645fb0aa - https://github.com/ethz-asl/kalibr

SMPLX Human Pose Estimation: pose estimation rgbd smplx
- [Real-time RGBD-based Extended Body Pose Estimation](https://arxiv.org/pdf/2103.03663.pdf)

[Few-shot Neural Human Performance Rendering from Sparse RGBD Videos](https://arxiv.org/pdf/2107.06505.pdf)


Dataset:
- https://github.com/YoYo000/BlendedMVS - MVSDepthNet
- http://cvlab.hanyang.ac.kr/project/omnistereo/
- Nerf in the wild: Phototourism dataset: https://www.cs.ubc.ca/research/image-matching-challenge/2021/data/

RGBD Dataset:
- https://github.com/kekeblom/StrayVisualizer
- https://github.com/hkust-vgd/scenenn
- http://redwood-data.org/indoor_lidar_rgbd/gallery.html
- http://3dvision.princeton.edu/datasets.html
- https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
- https://figshare.com/articles/dataset/Apple_iPhone_12_Pro_LiDAR_Test_Dataset/13382750/2

- broadcast and gather : https://pytorch.org/docs/stable/distributed.html, https://pytorch.org/tutorials/intermediate/dist_tuto.html



Try formulating this as a problem
- Modeling the 3D environment as Near and Far field would capture them better
- How to predict areas which are not seen or available for the Nerf to learn from?
- 

Basic ideas:
voxel grid for scene representation - nerf++

The 360 degree video failed because there are regions in the Nerf which are not encoded properly. So use a voxel based approach to identify which regions are visible which regions are not

Competing companies: https://www.linkedin.com/company/polycam/people/
- Simple mesh and image backpropagation can be a low quality output and then it an be iterated for better performance





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




Update website with the implementation details:
Current Baseline and Pitfalls
=============================
Colmap
Nerf++
Inference times
Training times
Time taken at each stage



https://arxiv.org/pdf/2004.00452.pdf - PiFUHD
https://arxiv.org/pdf/2103.13744.pdf - KiloNeRF
https://arxiv.org/pdf/2103.10380.pdf - fastNeRF

https://alexyu.net/plenoctrees/
https://nex-mpi.github.io/ - 
https://github.com/facebookresearch/NSVF - 


https://www.cs.cornell.edu/~zl548/NSFF/ - Neural Scene Flow Fields for Space-Time View Synthesis of Dynamic Scenes - Storing the video in neural network

Proposed solution:
=================
An unifying architecture which combines the capabilities of NeRF and 3D convolutions??

List of different Nerf Implementation:

(Nerf)[https://arxiv.org/pdf/2003.08934.pdf]
[Neural Sparse Voxel Fields](https://arxiv.org/pdf/2007.11571.pdf)

[Nerf++](https://arxiv.org/pdf/2010.07492.pdf)

- [KiloNeRF: Speeding up Neural Radiance Fields with Thousands of Tiny MLPs](https://github.com/creiser/kilonerf)
- [MVSNeRF](https://arxiv.org/pdf/2103.15595.pdf)
- [NeX: Real-time View Synthesis with Neural Basis Expansion](https://arxiv.org/pdf/2103.05606.pdf)
- [Baking Neural Radiance Fields for Real-Time View Synthesis](https://arxiv.org/pdf/2103.14645.pdf)
- [FastNerf](https://arxiv.org/pdf/2103.10380.pdf)
- [PlenOctrees: For Real-time Rendering of Neural Radiance Fields](https://alexyu.net/plenoctrees/)

[Neural Body](https://arxiv.org/pdf/2012.15838.pdf)
[Nerfies]

- [IBRNet: Learning Multi-View Image-Based Rendering](https://arxiv.org/pdf/2102.13090.pdf) -  - Read about this
- [MVSNeRF: Fast Generalizable Radiance Field Reconstruction from Multi-View Stereo](https://arxiv.org/pdf/2103.15595.pdf) - https://github.com/apchenstu/mvsnerf/blob/main/renderer.ipynb - this has result about all the implementation

Unifying surface rendering with volume rendering:
[UNISURF: Unifying Neural Implicit Surfaces and Radiance Fields for Multi-View Reconstruction](https://moechsle.github.io/unisurf/)
[Multiview Neural Surface Reconstruction by Disentangling Geometry and Appearance, Universal Differentiable Renderer for Implicit Neural Representations, UDR](https://arxiv.org/pdf/2003.09852.pdf)
[Multi-view 3D reconstruction using neural rendering. Unofficial implementation of UNISURF, VolSDF, NeuS and more.](https://pythonrepo.com/repo/ventusff-neurecon-python-imagery)


Estimating Camera parameters: Colmap, 
(Self calibraring neural radiance fields)[https://github.com/POSTECH-CVLab/SCNeRF], [paper](Self-Calibrating Neural Radiance Fields)
[Unofficial & improved implementation of NeRF--: Neural Radiance Fields Without Known Camera Parameters](https://pythonrepo.com/repo/ventusff-improved-nerfmm)
[NeRF−−: Neural Radiance Fields Without Known Camera Parameters](https://arxiv.org/pdf/2102.07064.pdf)
[BARF](https://chenhsuanlin.bitbucket.io/bundle-adjusting-NeRF/)
Pixel-Perfect Structure-from-Motion with Featuremetric Refinement [https://psarlin.com/pixsfm/], Back to the Feature [https://github.com/cvg/pixloc ?? Not sure]
- have a small network for predicting camera parameters like pose (like VIBE) using input image features and then use the camera parameters with nerf to check features
- Can you optimize sfm and nerf together
Nerf--, BaRF, 
- colmap exhautive_matcher seems to be consuming a lot of time - Optimized the using GPU


Input dimension: 3840x2160, 1920x1440

How to split voxel grid: Voxel based encoding:
- Can r, theta, phi representation instead of voxels?
- Nerf++: For nearby regions split it into voxels in the range 0-1 and for further parts make it from 1-inf
	- Splitting mechanism: num parts 10 => 1000 voxels, [1/r, 1/r^2, 1/r^3], [10, 100, 1000]/r
	- Can Octree be tried in the 1/r region
Resolution of the voxel grid: 


Use SiREN for faster convergence


Different NeRF Heads:
512x512 - NerfSH(PlenOctree) - Octree representation. Finally a single value for every tree node
Since we learn Spherical harmoics at each voxel, we just need to use triliniear interpolation to render the value in that position based on ray direction?

Baking NeRF[Sparse Neural Radiance Grid (SNrG)] - Grid of N^3 and data stored as MB of size B^3 for efficient access. Each voxel stores opacity, diffuse color (Cd), specular features (Vs)

The evaluation for direction based effects is done by a single neural network evaluation which sums the features along the ray and produces a color
Understand Specualr Features in SNrG, Spherical harmonics and Spherical gaussians in PlenOctree??

NexMex - Uses a set of planes - plane sweep which tries to model the transparency and the Shperical harmonics values k0, k1, kN. 
Mixed Implicit and explicit representation i.e. though they use a neural network to predict the k0, k1 etc and the alpha values they calculate it at fixed depths and store them in a array instead of directly using the neural network values. Further, they use the neural network for regularizing the k0, k1 and alpha values so that they do not overfit the data. 

The good thing from here is they try to learn their own radial basis funtion instead of standard basis like fourier or SH or Spherical gaussian. 

MVSNerf:
Uses neighboring images to extract convolutional features i.e. if we have to generate view for a particular camera position, it identifies three (M) nearby images homomorphically projects them all to the reference camera position and creates a Cost Volume. All the processing is from the reference point of view (No global view of the object). Then it uses the color information appended from the neighboring views to regress 

Mechanisms for faster inference:
- FastNerf: Caching techniques i.e. precalculating partial outputs for required directions and using that to optimze the rendering 

- Decoupling view dependent and view-independent parts of the network and precomputing the view dependent parts earlier and doing only the view dependent part

---------

Bayesian Optimization
Calculate inference from different camera views and choose the right set of images to learn [Bayesian optimization for choosing the right set of subset images]
To use bayesian optimization to find areas which need more learning
The camera position (x,y,z, axis angle representation) is the input (at a higher levels regions withing the camera could also be used)
The error values between predicted and the actual obtained during training could be used?
Sampling random areas within a image or using a downsampled image size to estimate the over all error based on the inference budget?
Inference is costly and so you cannot evaluate all the positions
As the training progresses the old values become better and so has to be reevaluated?
Can this be demonstrated with just nerf and assuming a infinite budget and training using images based on inference feedback evaluated at all positions ? Then if we make inference faster this can improve?


---------

non-visible voxels identification:
we render alpha maps for all the
training views using this voxel grid, keeping track of the
maximum ray weight 1 − exp(−σiδi) at each voxel. Compared to naively thresholding by σ at each point, this method eliminates non-visible voxels.


Module which evaluates the whole scene voxel by voxel and identifies voxels which have not been scene by the camera captured images
- this gives feedback on angles to take camera captures from
- can GANs or interpolation try filling these areas [Gan or Superresolution approaches for predicting intermediate unknown regions]


---------

Non-rigid body neural rendering:
- Extract features and map it to SMPLX
- We can adapt this to other non-rigid bodies like animals since they too have a mesh prior - like SMPL there is a mesh for babies and animals Facebook has such a representation
- We can add clothing related mesh prior assuming cloths of a particular form like free flowing etc and then apply this idea - There is a clothing prior
	- https://qianlim.github.io/SCALE, https://cape.is.tue.mpg.de/
- for using a single video - first register the person in their A pose or TPose and then use this info to map the person when he moves

------------

How is my method different from the earlier methods
- Trying to uses 2D features say from ResNet so there is a prior and so can learn faster
- Bayesian optimization since inference times are faster we can estimate where there are less quality and 
- Since we are using 2D features probably this will generalize across all the outputs
- Other than this we have removed the dependency on Colmap, and depth estimation for ray intersection with voxel or SMPLX since we are using Lidar and camera paramters from iPad Pro data

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




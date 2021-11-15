
## Deep Neural Radiance Field-based 3D Volumetric Video Capture, Rendering, and Streaming [Website](https://nitthilan.github.io/to_infinity_and_beyond/)



### Overview:

A user scans the 3D environment he wants to store, as a video capturing it from different viewing angles. He can use multiple cameras to capture more information about the environment like actions. We use artificial intelligence to reconstruct and encode the 3D environment using the different videos captured by the user. Unlike other methods which use laser or depth sensors to estimate point clouds, we just use the scanned RGB monocular videos to reconstruct the environment. Finally, this captured 3D environment is viewed using a VR headset in a 360-degree stereoscopic panorama. A stereoscopic photo is a pair of images, taken simultaneously with two lenses placed like our eyes, about 65 mm apart and looking in the same direction. When presented to the two eyes by a stereoscope, these images give most people the impression of seeing a 3D space. A stereoscopic panorama is a pair of 360-degree images, which when viewed with synchronized pano viewers (like a VR headset) presents a stereo pair. Further, as the user moves around in the environment, we generate the corresponding stereo pair based on the user position to give the user an immersive 3D experience

### Modules: [details]([Website](https://nitthilan.github.io/to_infinity_and_beyond/))

#### Multi-view capture system

#### Split neural encoder, renderer and compositor

#### 360 Stereo video encoder


### Folder structure:

#### Pre-processing:

- Colmap - Used code from [nerf++](https://github.com/Kai-46/nerfplusplus). The input video is pre-processed by splitting into multiple images and the corresponding camera parameters are estimated. The folder has utilities that help in this estimation

#### Encoder:

- nerf-pytorch - Pytorch implementation of nerf code taken from [nerf-pytorch](https://github.com/yenchenlin/nerf-pytorch)
- nerfplusplus - Pytorch implementation of nerf code taken from [nerf++](https://github.com/Kai-46/nerfplusplus)
- nerf_roxel - Proposed voxel based nerf for capturing the whole scene


#### VR endpoint:

- stereo_photo_app - Unity application for receiving 360-degree panorama stereo photos and displaying them on a VR headset. Currently using Occulus 2



### Task list:


- colmap exhautive_matcher seems to be consuming a lot of time - Optimized the using GPU

- http://cvlab.hanyang.ac.kr/project/omnistereo/ - dataset

- Nerf in the wild: Phototourism dataset: https://www.cs.ubc.ca/research/image-matching-challenge/2021/data/

- broadcast and gather : https://pytorch.org/docs/stable/distributed.html, https://pytorch.org/tutorials/intermediate/dist_tuto.html

Using 3D convolution and nerf together
Using r,theta,phi representation instead of voxels
Can you optimize sfm and nerf together

have a small network for predicting camera parameters like pose (like VIBE) using input image features and then use the camera parameters with nerf to check features

Try formulating this as a problem


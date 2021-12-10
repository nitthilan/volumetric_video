import torch
import torch.nn as nn
from torchvision.models import resnet50



# Choose a image feature generator
# - Trying out pre-trained networks from image net
# - Would replace it with U-Net based segmentation networks
# 


def create_feature_generator(rank):
    resnet = resnet50(pretrained = True)
    # print("train_nodes ", rank)
    # print("Model layers ", list(resnet.children()), len(list(resnet.children())))

    modules = list(resnet.children())[:-2] # delete the last two layers.
    resnet = nn.Sequential(*modules)
    ### Now set requires_grad to false
    for param in resnet.parameters():
        param.requires_grad = False

    # resnet = DDP(resnet, device_ids=[rank], output_device=rank, find_unused_parameters=True)


    return resnet.to(rank)

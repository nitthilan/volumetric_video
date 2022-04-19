import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl
import dataloader as dl
from pytorch_lightning.callbacks import ModelCheckpoint
import network as net
import occupancy as occ
from torchvision.transforms import ToPILImage


def dump_image(rgb, name, wth=int(1920/4), hgt=int(1440/4)):
    rgb = rgb.detach()
    rgb = rgb.reshape(hgt, wth, -1)
    rgb = torch.transpose(rgb, 0, 2)
    rgb = ToPILImage()(rgb)
    rgb.save(name)
    # save_image(rgb, 'rgb' + str(idx) + '.png')
    return


if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description="Train a surf voxel encoder")
    arg_parser.add_argument( "--data_dir", "-d", dest="data_dir",  required=True,
        default="./", help="Data directory base")
    arg_parser.add_argument( "--config", "-cfg", dest="cfg_path",  required=True,
        default="./tcn_config.json", help="Network configuration path")
    arg_parser.add_argument( "--continue", "-c", dest="cont_frm", # required=True,
        default="./checkpoints/", help="Continue from learned model")
    args = arg_parser.parse_args()


    skip = 1
    resolution_level = 4
    confidence_level = 1
    max_depth = 4.0
    voxel_size = 0.05
    max_hits = 40
    batch_size = 10
    num_train_sample = 1500
    truncation = 1.0
    sc_factor = 0.05


    val_dl = dl.NVSD(args.data_dir, skip=skip, split="val", resolution_level = resolution_level, \
        confidence_level = confidence_level, max_depth=max_depth)
    dataset = val_dl.get_full_data(0)
    box_min_off = dataset['box_min_off']
    box_dim = dataset['box_dim']


    num_frames = 860 #522 # hardcoded

    # torch.save(voxel_base_xyz, 'occupancy.pt')
    # voxel_base_xyz = torch.load('occupancy_3depth.pt')
    voxel_base_xyz = torch.load('cor_occupancy.pt')
    # print("voxel xyz ", voxel_base_xyz[:10])
    
    # ckpt_file_path = "./checkpoints/ckpts_nvse_enc_epoch=0535_val_loss=0.0080.ckpt"
    # ckpt_file_path = "./checkpoints_ct_100/last.ckpt"
    # ckpt_file_path = "./checkpoints_ct/ckpts_nvse_enc_epoch=0278_val_loss=0.0021.ckpt"
    # ckpt_file_path = "./checkpoints_ct_100/ckpts_nvse_enc_epoch=0030_val_loss=0.0020.ckpt"

    # ckpt_file_path = "./ckpts_ct_100_res_2/nvse_enc_epoch=0005_val_loss=0.0137.ckpt"
    ckpt_file_path = "./ckpts_ct_100_occ/nvse_enc_epoch=0011_val_loss=0.0079.ckpt"
    # ckpt_file_path = "./ckpts_ct_100_occ/last.ckpt"
    ckpt_file_path = "./ckpts_ct_100_occ_sdf_lr/last.ckpt"
    

    nvse_net = net.NVSEnc.load_from_checkpoint(ckpt_file_path, config_path = args.cfg_path, 
        num_frames = num_frames, voxel_size=voxel_size, voxel_base_xyz=voxel_base_xyz, box_min_off=box_min_off,
        box_dim=box_dim, max_hits=max_hits, resolution_level=resolution_level,
        sc_factor=sc_factor, truncation=truncation, max_depth=max_depth)

    device = "cuda:0"

    nvse_net.eval().to(device)
    for i, batch in enumerate(val_dl):
        batch['ray_d'] = batch['ray_d'].unsqueeze(0).to(device)
        batch['depth'] = batch['depth'].unsqueeze(0).to(device)
        batch['rgb'] = batch['rgb'].unsqueeze(0).to(device)
        batch['ray_o'] = batch['ray_o'].unsqueeze(0).to(device)
        batch['box_min_off'] = batch['box_min_off'].unsqueeze(0).to(device)
        batch['box_dim'] = batch['box_dim'].unsqueeze(0).to(device)
        batch['valid_depth'] = batch['valid_depth'].unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = nvse_net.validation_step(batch, i)
            print(outputs['val_loss'], batch['file_idx'])
            dump_image(outputs['pred_rgb'], './inference/rgb_' + str(i)   + '.png',
                wth=int(1920/resolution_level), hgt=int(1440/resolution_level))

            dump_image(outputs['depth'], './inference/depth_' + str(i)   + '.png',
                wth=int(1920/resolution_level), hgt=int(1440/resolution_level))
            
            # print("Min max depth ", torch.min(outputs['depth']), torch.max(outputs['depth']))


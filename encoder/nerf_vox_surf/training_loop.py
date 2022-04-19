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
    resolution_level = 8
    confidence_level = 2
    max_depth = 4.0
    voxel_size = 0.05
    max_hits = 40
    batch_size = 6 #13 #
    num_train_sample = 5000
    truncation = 1.0
    sc_factor = 0.05
    num_workers = 32


    tr_dl = dl.NVSD(args.data_dir, skip=skip, split="train", resolution_level = resolution_level, \
        confidence_level = confidence_level, max_depth=max_depth)
    dataset = tr_dl.get_full_data(0)
    box_min_off = dataset['box_min_off']
    box_dim = dataset['box_dim']



    nvsdm = dl.NVSDM(args.data_dir, skip=skip, resolution_level=resolution_level, 
        confidence_level=confidence_level, batch_size=batch_size, num_workers=num_workers, 
        max_depth=(max_depth+voxel_size), num_train_sample=num_train_sample)

    num_frames = 860 #522 # hardcoded

    # voxel_base_xyz = occ.calculate_occupancy(tr_dl=tr_dl, 
    #     confidence_level=confidence_level, max_depth=max_depth, voxel_size=voxel_size)
    # torch.save(voxel_base_xyz, 'cor_occupancy.pt')
    # voxel_base_xyz = torch.load('occupancy_3depth.pt')
    voxel_base_xyz = torch.load('cor_occupancy.pt')
    # print("voxel xyz ", voxel_base_xyz[:10])

    # occ.validate_occupancy(tr_dl=tr_dl, confidence_level=confidence_level, 
    #     scene_max_depth=max_depth, voxel_size=voxel_size, voxel_base_xyz=voxel_base_xyz,
    #     max_hits=max_hits)

    # exit()

    # init model
    nvse_net = net.NVSEnc(config_path = args.cfg_path, num_frames = num_frames,
        voxel_size=voxel_size, voxel_base_xyz=voxel_base_xyz, box_min_off=box_min_off,
        box_dim=box_dim, max_hits=max_hits, resolution_level=resolution_level,
        sc_factor=sc_factor, truncation=truncation, max_depth=max_depth)
    
    # ckpt_file_path = "./checkpoints/ckpts_nvse_enc_epoch=0535_val_loss=0.0080.ckpt"
    # ckpt_file_path = "./checkpoints_ct/ckpts_nvse_enc_epoch=0278_val_loss=0.0021.ckpt"
    # ckpt_file_path = "./checkpoints_ct_100/ckpts_nvse_enc_epoch=0030_val_loss=0.0020.ckpt"
    # ckpt_file_path = "./ckpts_ct_100_occ_sdf_lr/last_lr_4.ckpt"
    # nvse_net = net.NVSEnc.load_from_checkpoint(ckpt_file_path, config_path = args.cfg_path, 
    #     num_frames = num_frames, voxel_size=voxel_size, voxel_base_xyz=voxel_base_xyz, box_min_off=box_min_off,
    #     box_dim=box_dim, max_hits=max_hits, resolution_level=resolution_level,
    #     sc_factor=sc_factor, truncation=truncation, max_depth=max_depth)


    ckpt_filename = "nvse_enc"
    # saves a file like: my/path/sample-mnist-epoch=02-val_loss=0.32.ckpt
    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath="./ckpts_ct_100_occ_sdf_lr/",
        filename=ckpt_filename+"_{epoch:04d}_{val_loss:.4f}",
        save_top_k=3,
        mode="min",
        save_last=True
    )

    # most basic trainer, uses good defaults (auto-tensorboard, checkpoints, logs, and more)
    # trainer = pl.Trainer(gpus=8) (if you have GPUs)
    trainer = pl.Trainer(gpus=1, accelerator='ddp', max_epochs=10000,
        callbacks=[checkpoint_callback]) # num_processes=8, - num cpu, precision=16
    trainer.fit(nvse_net, nvsdm)
    # print("Output check point ", dir(checkpoint_callback))

    # trainer.test(datamodule=nvsdm)



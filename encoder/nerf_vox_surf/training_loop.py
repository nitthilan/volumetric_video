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


if __name__ == "__main__":

    import argparse

    arg_parser = argparse.ArgumentParser(description="Train a surf voxel encoder")
    arg_parser.add_argument( "--experiment", "-e", dest="expt_dir", # required=True,
        default="./", help="Directory base")
    arg_parser.add_argument( "--data_dir", "-d", dest="data_dir",  required=True,
        default="./", help="Data directory base")
    arg_parser.add_argument( "--config", "-cfg", dest="cfg_path",  required=True,
        default="./tcn_config.json", help="Network configuration path")
    arg_parser.add_argument( "--continue", "-c", dest="cont_frm", # required=True,
        default="./checkpoints/", help="Continue from learned model")
    arg_parser.add_argument( "--batch_split", "-b", dest="batch_split", default=1,
        help="Batch split data",)
    args = arg_parser.parse_args()

    nvsdm = dl.NVSDM(args.data_dir, skip=1, resolution_level=4, confidence_level=1,
        batch_size=1, num_workers=4)

    # init model
    nvse_net = net.NVSEnc(config_path = args.cfg_path)


    ckpt_filename = "ckpts_nvse_enc"
    # saves a file like: my/path/sample-mnist-epoch=02-val_loss=0.32.ckpt
    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath="./checkpoints/",
        filename=ckpt_filename+"_{epoch:04d}_{val_loss:.4f}",
        save_top_k=3,
        mode="min",
    )

    # most basic trainer, uses good defaults (auto-tensorboard, checkpoints, logs, and more)
    # trainer = pl.Trainer(gpus=8) (if you have GPUs)
    trainer = pl.Trainer(gpus=1, accelerator='ddp', max_epochs=10000,
        callbacks=[checkpoint_callback]) # num_processes=8, - num cpu, precision=16
    trainer.fit(nvse_net, nvsdm)

    # trainer.test(datamodule=nvsdm)



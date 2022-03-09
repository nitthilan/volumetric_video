#!/usr/bin/env python3

import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np
import pytorch_lightning as pl
import json
import volume_rendering as vr
from torch_ema import ExponentialMovingAverage


try:
    import tinycudann as tcnn
except ImportError:
    print("This sample requires the tiny-cuda-nn extension for PyTorch.")
    print("You can install it by running:")
    print("============================================================")
    print("tiny-cuda-nn$ cd bindings/torch")
    print("tiny-cuda-nn/bindings/torch$ python setup.py install")
    print("============================================================")
    sys.exit()


class NVSEnc(pl.LightningModule):

    def __init__(self, config_path, num_frames):
        super().__init__()

        with open(config_path) as config_file:
            config = json.load(config_file)

        self.n_den_inp = 3 # num channels of input density
        self.n_den_out = 16 # density network output channels
        self.den_net = tcnn.NetworkWithInputEncoding(self.n_den_inp, 
            self.n_den_out, encoding_config=config["encoding"], 
            network_config=config["network"])

        self.n_dir_inp = 3
        self.n_rgb_out = 3
        self.rgb_enc = tcnn.Encoding(self.n_dir_inp, config["dir_encoding"])
        n_rgb_inp = self.rgb_enc.n_output_dims + self.n_den_out
        self.rgb_net = tcnn.Network(n_rgb_inp, self.n_rgb_out, config["rgb_network"])
        print(self.den_net)
        print(self.rgb_enc)
        print(self.rgb_net)
        # print(self.rgb_enc.n_output_dims, )

        # Latent Variable for frames
        frm_emb_dim = 16
        self.frm_emb = nn.Embedding(num_frames, frm_emb_dim)

        # Pose correction embedding for frames [0:3] - translation 
        # [3:6] - alpha, beta, gamma
        self.pose_correction = nn.Embedding(num_frames, 6)



        self.config = config
        # self.optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        self.params = list(self.den_net.parameters()) + list(self.rgb_enc.parameters()) \
            + list(self.rgb_net.parameters())
        self.ema = ExponentialMovingAverage(self.params, decay=0.995)
        self.ce_loss = nn.CrossEntropyLoss()

    def on_before_zero_grad(self, *args, **kwargs):
        self.ema.update(self.params)

    def forward(self, batch):
                # print(batch.keys(), batch_idx, batch['ray_o'].shape, 
        #     batch['ray_d'].shape, batch['depth'].shape,
        #     batch['ray_o'].unsqueeze(1).shape, 
        #     batch['depth'].unsqueeze(-1).shape)
        num_pts_per_ray = 16
        resolution = 0.5 #0.001
        sample = torch.linspace(0, 1, num_pts_per_ray).to(batch['ray_d'].device) 
        sample = sample - sample[int(num_pts_per_ray/2)]
        sample = sample*resolution
        depth_pred = torch.zeros_like(sample).to(batch['ray_d'].device)
        depth_pred[int(num_pts_per_ray/2)] = 1.0

        print("Sample ", sample/torch.norm(batch['box_dim']))

        # print(batch['ray_d'].unsqueeze(-2).shape, 
        #     sample.unsqueeze(0).unsqueeze(0).unsqueeze(-1).shape)
        offsets = batch['ray_d'].unsqueeze(-2) * sample.unsqueeze(0).unsqueeze(0).unsqueeze(-1)
        # print(sample[25:35], offsets.shape) 

        base_offset = batch['ray_o'].unsqueeze(1) + \
            batch['ray_d']*batch['depth'].unsqueeze(-1)
        sample_offset = (base_offset.unsqueeze(-2) + offsets)
        # print(base_offset.shape, sample_offset.shape, offsets.shape)

        # print(base_offset[0,:2], batch['ray_o'], batch['ray_d'][0,:2], batch['depth'][0,:2])
        # print(offsets[0,:2])
        # print(sample_offset[0,:2])

        sample_offset = (sample_offset - batch['box_min_off'])/batch['box_dim']

        num_batch, img_sam, ray_sam, _ = sample_offset.shape
        sample_offset = sample_offset.reshape(-1, 3)
        # print(sample_offset.shape, batch['ray_d'].shape)
        if(torch.min(sample_offset) < 0.0 or torch.max(sample_offset) > 1.0):
            print("Sample offset min and max ", torch.min(sample_offset, dim=0),
                torch.max(sample_offset, dim=0))

        den_out = self.den_net(sample_offset)
        # print("Density min and max ", torch.min(den_out, dim=0),
        #     torch.max(den_out, dim=0))

        dir_inp = batch['ray_d'].unsqueeze(-2).repeat(1,1,ray_sam,1)
        # print(dir_inp.shape)
        dir_inp = dir_inp.reshape(-1, 3)
        dir_enc = self.rgb_enc(dir_inp)

        rgb_inp = torch.cat((den_out, dir_enc), -1)
        rgb_out = self.rgb_net(rgb_inp)
        # print(den_out.shape, dir_enc.shape, rgb_inp.shape, rgb_out.shape)

        rgb_out = rgb_out.reshape(num_batch, img_sam, ray_sam, -1)
        den_out = den_out.reshape(num_batch, img_sam, ray_sam, -1)
        # radiance_field = torch.cat((rgb_out, den_out[..., :1]), -1)

        # print("Radiance field min and max ", torch.min(radiance_field, dim=1),
        #     torch.max(radiance_field, dim=1))
        depth_offset = sample.unsqueeze(0).unsqueeze(0).repeat(num_batch,img_sam,1) + \
            batch['depth'].unsqueeze(-1).repeat(1,1,ray_sam)
        # dir_inp = dir_inp.reshape(num_batch, img_sam, ray_sam, -1)
        # print(radiance_field.shape, depth_offset.shape)
        # print(depth_offset[0,:2])
        # depth_offset = depth_offset/torch.norm(batch['box_dim'])

        rgb_map, disp_map, acc_map, weights, depth_map, alpha = \
            vr.volume_render_radiance_field( rgb_out, den_out[..., 1],
                depth_offset, radiance_field_noise_std=1.0, white_background=False)

        # print(rgb_map.shape)
        # training_step defined the train loop.
        # It is independent of forward
        # x, y = batch
        # # x = x.view(x.size(0), -1)
        # y_hat = self.forward(x)
        # # print(x.shape, y.shape, y_hat.squeeze().shape)
        # # loss = F.mse_loss(y_hat.squeeze(), y)
        # loss = F.l1_loss(y_hat.squeeze(), y)
        # # print(y_hat.squeeze()[:10], y[:10], x.shape)
        # # Logging to TensorBoard by default
        # self.log('train_loss', loss)
        

        # output = self.forward(batch)

        # relative_l2_error = (output - targets.to(output.dtype))**2 / (output.detach()**2 + 0.01)
        # loss = relative_l2_error.mean()

        # print(depth_map[0, :10])
        # print(batch['depth'][0, :10])

        # print(rgb_map[0, :10])
        # print(batch['rgb'][0, :10])
        rgb_loss = F.mse_loss(rgb_map, batch['rgb'])
        depth_loss = F.mse_loss(depth_map, batch['depth'])
        alpha_loss = F.mse_loss(alpha, \
            depth_pred.unsqueeze(0).unsqueeze(0).repeat(1,img_sam,1))
        # alpha_loss = self.ce_loss(alpha, 
        #     depth_pred.unsqueeze(0).unsqueeze(0).repeat(1,img_sam,1))
        loss = 0.0*depth_loss + 0.0*rgb_loss + alpha_loss
        # print(depth_loss, rgb_loss, alpha_loss)
        # print(depth_pred.unsqueeze(0).unsqueeze(0).repeat(1,img_sam,1).shape, alpha.shape)

        # print("rgb min and max ", torch.min(rgb_map, dim=1),
        #     torch.max(rgb_map, dim=1))
        # print("batch rgb min and max ", torch.min(batch['rgb'], dim=1),
        #     torch.max(batch['rgb'], dim=1))

        tqdm_dict = {'train_loss': loss}
        outputs = {
            'loss': loss,
            'progress_bar': tqdm_dict,
            'log': tqdm_dict
        }


        return outputs

    def training_step(self, batch, batch_idx):

        outputs = self.forward(batch)
        return outputs['loss']

    # def training_epoch_end(self, training_step_outputs):
    #     for prediction in training_step_outputs:
    #         # do something with these
    #         print (prediction)

    #     return

    def validation_step(self, batch, batch_idx):
        outputs = self.forward(batch)
        return outputs

    def validation_epoch_end(self, outputs):
        # print("Output ", outputs)
        avg_loss = torch.stack([x['loss'] for x in outputs]).mean()
        tqdm_dict = {'val_loss': avg_loss}
        print("Val loss ", avg_loss)

        return {
                'progress_bar': tqdm_dict,
                'log': {'avg_val': avg_loss},
        }


    def configure_optimizers(self):
        params = list(self.den_net.parameters()) + list(self.rgb_enc.parameters()) \
            + list(self.rgb_net.parameters())
        optimizer = torch.optim.Adam(params, lr=0.001, eps=1e-15, 
            betas=(0.9, 0.995), weight_decay=1e-6)
        # optimizer = torch.optim.Adam(self.parameters(), lr=0.01)
        return optimizer


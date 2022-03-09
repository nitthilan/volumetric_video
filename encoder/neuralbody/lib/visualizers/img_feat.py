import matplotlib.pyplot as plt
import numpy as np
from lib.config import cfg
from PIL import Image



class Visualizer:
    def __init__(self):
        self.img_num = 0
    def visualize(self, output, batch):
        rgb_pred = output['rgb_map'][0].detach().cpu().numpy()
        rgb_gt = batch['rgb'][0].detach().cpu().numpy()
        print('mse: {}'.format(np.mean((rgb_pred - rgb_gt) ** 2)))
        
        depth = batch['depth'][0].detach().cpu().numpy()
        H, W = int(1440 * 1/cfg.ratio), int(1920 * 1/cfg.ratio)
        # mask_at_box = mask_at_box.reshape(H, W)

        # print("Image shape ", rgb_pred.shape, rgb_gt.shape, depth.shape,
        #     np.sum(depth!=0), H, W)

        img_pred = np.zeros((H, W, 3)).reshape((-1, 3))
        # if cfg.white_bkgd:
        #     img_pred = img_pred + 1
        img_pred[depth != 0, :] = rgb_pred
        img_pred = img_pred.reshape((H,W,3))

        img_gt = np.zeros((H, W, 3)).reshape((-1, 3))
        # if cfg.white_bkgd:
        #     img_gt = img_gt + 1
        img_gt[depth != 0, :] = rgb_gt
        img_gt = img_gt.reshape((H,W,3))

        result = Image.fromarray((img_pred * 255).astype(np.uint8))
        result.save('./data/output/out_'+str(self.img_num)+'.bmp')
        self.img_num += 1

        # _, (ax1, ax2) = plt.subplots(1, 2)
        # ax1.imshow(img_pred)
        # ax2.imshow(img_gt)
        # plt.show()

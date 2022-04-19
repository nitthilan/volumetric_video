import torch
import torch.nn.functional as F



def compute_loss(prediction, target, loss_type='l2'):
    if loss_type == 'l2':
        return F.mse_loss(prediction, target)
    elif loss_type == 'l1':
        return F.mae_loss(prediction, target)

    raise Exception('Unsupported loss type')


def get_masks(z_vals, target_d, truncation):

    front_mask = torch.where(z_vals < (target_d - truncation), torch.ones_like(z_vals), torch.zeros_like(z_vals))
    back_mask = torch.where(z_vals > (target_d + truncation), torch.ones_like(z_vals), torch.zeros_like(z_vals))
    depth_mask = torch.where(target_d > 0.0, torch.ones_like(target_d), torch.zeros_like(target_d))
    sdf_mask = (1.0 - front_mask) * (1.0 - back_mask) * depth_mask

    num_fs_samples = torch.count_nonzero(front_mask)
    num_sdf_samples = torch.count_nonzero(sdf_mask)
    num_samples = num_sdf_samples + num_fs_samples
    total_samples = z_vals.shape[0]*z_vals.shape[1]

    fs_weight = total_samples / num_fs_samples # 1.0 - num_fs_samples / num_samples
    sdf_weight = total_samples / num_sdf_samples # 1.0 - num_sdf_samples / num_samples

    # print("weights ", num_sdf_samples, num_fs_samples, num_samples,
    #     fs_weight, sdf_weight)

    return front_mask, sdf_mask, fs_weight, sdf_weight


def get_sdf_loss(z_vals, target_d, predicted_sdf, truncation, loss_type='l2'):

    front_mask, sdf_mask, fs_weight, sdf_weight = get_masks(z_vals, target_d, truncation)

    fs_loss = compute_loss(predicted_sdf * front_mask, torch.ones_like(predicted_sdf) * front_mask, loss_type) * fs_weight
    sdf_loss = compute_loss((z_vals + predicted_sdf * truncation) * sdf_mask, target_d * sdf_mask, loss_type) * sdf_weight

    # print("SDF ", (z_vals + predicted_sdf * truncation).shape, target_d.shape, predicted_sdf.shape,
    #     z_vals.shape, sdf_mask.shape, (target_d * sdf_mask).shape, truncation)
    
    # print(target_d[0,:2, :5])
    # print((target_d * sdf_mask)[0, :2, -10:])
    # print(sdf_mask[0, :2, -10:])
    # print(z_vals[0, :2, -10:])
    # print(predicted_sdf[0, :2, -10:])
    # print(sdf_loss, sdf_weight)

    return fs_loss, sdf_loss


def get_depth_loss(predicted_depth, target_d, loss_type='l2'):
    depth_mask = torch.where(target_d > 0, torch.ones_like(target_d), torch.zeros_like(target_d))
    eps = 1e-4
    num_pixel = depth_mask.shape[0]
    num_valid = torch.count_nonzero(depth_mask) + eps
    depth_valid_weight = num_pixel / num_valid

    return compute_loss(predicted_depth * depth_mask, target_d * depth_mask, loss_type) * depth_valid_weight


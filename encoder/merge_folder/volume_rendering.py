import torch


def cumprod_exclusive(tensor: torch.Tensor) -> torch.Tensor:
    r"""Mimick functionality of tf.math.cumprod(..., exclusive=True), as it isn't available in PyTorch.

    Args:
    tensor (torch.Tensor): Tensor whose cumprod (cumulative product, see `torch.cumprod`) along dim=-1
      is to be computed.

    Returns:
    cumprod (torch.Tensor): cumprod of Tensor along dim=-1, mimiciking the functionality of
      tf.math.cumprod(..., exclusive=True) (see `tf.math.cumprod` for details).
    """
    # TESTED
    # Only works for the last dimension (dim=-1)
    dim = -1
    # Compute regular cumprod first (this is equivalent to `tf.math.cumprod(..., exclusive=False)`).
    cumprod = torch.cumprod(tensor, dim)
    # "Roll" the elements along dimension 'dim' by 1 element.
    cumprod = torch.roll(cumprod, 1, dim)
    # Replace the first element by "1" as this is what tf.cumprod(..., exclusive=True) does.
    cumprod[..., 0] = 1.0

    return cumprod


def sdf2weights(sdf):
    weights = tf.math.sigmoid(sdf / truncation) * tf.math.sigmoid(-sdf / truncation)

    signs = sdf[:, 1:] * sdf[:, :-1]
    mask = tf.where(signs < 0.0, tf.ones_like(signs), tf.zeros_like(signs))
    inds = tf.math.argmax(mask, axis=1)
    inds = inds[..., tf.newaxis]
    z_min = tf.gather(z_vals, inds, axis=1, batch_dims=1)
    mask = tf.where(z_vals < z_min + sc_factor * truncation, tf.ones_like(z_vals), tf.zeros_like(z_vals))

    weights = weights * mask
    return weights / (tf.reduce_sum(weights, axis=-1, keepdims=True) + 1e-8)


def volume_render_radiance_field(
    rgb_in, sigma_in,
    depth_values,
    # ray_directions,
    radiance_field_noise_std=0.0,
    white_background=False,
):
    # TESTED
    # one_e_10 = torch.tensor(
    #     [1e2], dtype=rgb_in.dtype, device=rgb_in.device
    # )
    # dists = torch.cat(
    #     (
    #         depth_values[..., 1:] - depth_values[..., :-1],
    #         one_e_10.expand(depth_values[..., :1].shape),
    #     ),
    #     dim=-1,
    # )
    zero_tensor = torch.tensor(
        [0.0], dtype=rgb_in.dtype, device=rgb_in.device
    )
    dists = torch.cat(
        (
            depth_values[..., 1:] - depth_values[..., :-1],
            zero_tensor.expand(depth_values[..., :1].shape),
        ),
        dim=-1,
    )
    
    # dists = dists * ray_directions[..., None, :].norm(p=2, dim=-1)
    # dists = dists.norm(p=2, dim=-1)

    rgb = torch.sigmoid(rgb_in)

    # weights = sdf2weights(raw[..., 3])

    noise = 0.0
    radiance_field_noise_std = 1.0
    if radiance_field_noise_std > 0.0:
        noise = (
            torch.randn(
                sigma_in.shape,
                dtype=rgb_in.dtype,
                device=rgb_in.device,
            )
            * radiance_field_noise_std
        )
        # noise = noise.to(radiance_field)
    sigma_a = torch.nn.functional.relu(sigma_in + noise)
    # print(sigma_a.shape, dists.shape) 
    # alpha = 1.0 - torch.exp(-sigma_a * dists * 7.0)
    # weights = alpha * cumprod_exclusive(1.0 - alpha + 1e-10)


    free_energy = torch.relu(sigma_in + noise) * dists * 7.0
    # print("Input shapes ", free_energy.shape, depth_values.shape, free_energy.new_zeros(depth_values.size(0), 1).shape)
    shifted_free_energy = torch.cat([free_energy.new_zeros(depth_values.size(0), depth_values.size(1), 1), free_energy[:, :, :-1]], dim=-1)  # shift one step
    a = 1 - torch.exp(-free_energy.float())                             # probability of it is not empty here
    b = torch.exp(-torch.cumsum(shifted_free_energy.float(), dim=-1))   # probability of everything is empty up to now
    weights = (a * b).type_as(free_energy)                                # probability of the ray hits something here
    alpha = a


    # print("shapes ", radiance_field.shape, alpha.shape, rgb.shape, dists.shape,
    #     one_e_10)
    # print("depth_values min and max ", torch.min(depth_values, dim=1),
    #         torch.max(depth_values, dim=1))
    # print("radiance_field min and max ", torch.min(radiance_field, dim=1),
    #         torch.max(radiance_field, dim=1))
    # print("alpha min and max ", torch.min(alpha, dim=1),
    #         torch.max(alpha, dim=1))
    # print("rgb min and max ", torch.min(rgb, dim=1),
    #         torch.max(rgb, dim=1))
    # print("dists min and max ", torch.min(dists, dim=1),
    #         torch.max(dists, dim=1))

    rgb_map = weights[..., None] * rgb
    rgb_map = rgb_map.sum(dim=-2)
    depth_map = weights * depth_values
    depth_map = depth_map.sum(dim=-1)
    # depth_map = (weights * depth_values).sum(dim=-1)
    acc_map = weights.sum(dim=-1)
    disp_map = 1.0 / torch.max(1e-10 * torch.ones_like(depth_map), depth_map / acc_map)

    if white_background:
        rgb_map = rgb_map + (1.0 - acc_map[..., None])

    # print("shapes ", acc_map.shape, weights.shape, depth_map.shape, rgb_map.shape)
    # print(torch.max(weights, dim=-1))
    # print(weights[0, :10, ])
    
    # print(alpha[0, :10, ])
    # print(cumprod_exclusive(1.0 - alpha + 1e-10)[0, :10, ])
    # print(sigma_a[0, :10, ])
    # print(dists[0, :10, ])
    # print(depth_values[0, :10, ])
    # print(depth_map[0, :10])
    # print()

    return rgb_map, disp_map, acc_map, weights, depth_map, alpha

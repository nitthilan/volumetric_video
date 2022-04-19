import torch



def sdf2weights(sdf, z_vals, sc_factor, truncation):
    weights = torch.sigmoid(sdf / truncation) * torch.sigmoid(-sdf / truncation)

    signs = sdf[:, :, 1:] * sdf[:, :, :-1]
    mask = torch.where(signs < 0.0, torch.ones_like(signs), torch.zeros_like(signs))
    inds = torch.argmax(mask, dim=-1)
    inds = inds[..., None]
    z_min = torch.gather(z_vals, dim=-1, index=inds)
    mask = torch.where(z_vals < z_min + sc_factor * truncation, torch.ones_like(z_vals), torch.zeros_like(z_vals))

    weights = weights * mask
    return weights / (torch.sum(weights, dim=-1).unsqueeze(-1) + 1e-8)


def raw2weights(sigma_in, dists):
    noise = 0.0
    radiance_field_noise_std = 1.0
    if radiance_field_noise_std > 0.0:
        noise = (
            torch.randn(
                sigma_in.shape,
                dtype=sigma_in.dtype,
                device=sigma_in.device,
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
    shifted_free_energy = torch.cat([free_energy.new_zeros(sigma_in.size(0), sigma_in.size(1), 1), free_energy[:, :, :-1]], dim=-1)  # shift one step
    a = 1 - torch.exp(-free_energy.float())                             # probability of it is not empty here
    b = torch.exp(-torch.cumsum(shifted_free_energy.float(), dim=-1))   # probability of everything is empty up to now
    weights = (a * b).type_as(free_energy)                                # probability of the ray hits something here
    alpha = a

    return weights

def volume_render_radiance_field(
    rgb_in, sigma_in,
    depth_values,
    # ray_directions,
    radiance_field_noise_std=0.0,
    white_background=False,
    sc_factor=0.05, truncation=1.0,
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

    # weights = raw2weights(sigma_in, dists)
    weights = sdf2weights(sigma_in, depth_values, sc_factor, truncation)


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

    return rgb_map, disp_map, acc_map, weights, depth_map

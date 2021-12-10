import os
import imp


def make_feat_gen(cfg, bbox):
    module = cfg.feat_gen.module
    path = cfg.feat_gen.path
    feat_gen = imp.load_source(module, path).FeatGen(bbox, cfg.voxel_size)
    return feat_gen

#!/usr/bin/env python
import sys
import os

import argparse
from classes.FeaturizedObject import FeaturizedObject
from visualization.compare_visualizer import CompareVisualizer
import imageio
import numpy as np

def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--box2d_data_path", help="the path of the log file or directory", type=str,
                        default='box2d_data')
    parser.add_argument("--nn_data_path", type=str,
                        default='nn_rollout')
    parser.add_argument("--log_path", type=str, default='gine5-task1-1x100')
    #parser.add_argument("--tasks_label", type=str, default="1-1x100")
    parser.add_argument('--exp_name',type=str, default='gine_bn_')
    parser.add_argument("--dir", help="the path is a directory or not", action="store_true", default=True)
    parser.add_argument("--image", help="generating images", action="store_true", default=False)
    parser.add_argument("--gif", help="generating gifs", action="store_true", default=True)

    config = parser.parse_args()
    return config


#def compare(raw_dataset_name, exp_name, root_dir='/home/yiran/pc_mapping/GenBox2D/src/main/python'):
def compare(config):
    visualizer = CompareVisualizer(config, config.box2d_root_dir)

    if config.dir:
        visualizer.replay_dir()
    else:
        visualizer.replay_file()


if __name__ == '__main__':
    config = get_config_from_args()
    compare(raw_dataset_name='0-11x100', exp_name='gine_ev_ep40_lr0.001000_h128_0-11x100-ep25')

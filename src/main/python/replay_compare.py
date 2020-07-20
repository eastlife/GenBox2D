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
    parser.add_argument("--log_path", type=str, default='GIN5-task1-1x100')
    parser.add_argument("--tasks_label", type=str, default="1-1x100")
    parser.add_argument("--compare_path", type=str,
                        default='compare/')
    parser.add_argument("--dir", help="the path is a directory or not", action="store_true", default=True)
    parser.add_argument("--image", help="generating images", action="store_true", default=False)
    parser.add_argument("--gif", help="generating gifs", action="store_true", default=True)
    parser.add_argument("--name_prefix", type=str, default='')

    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()
    visualizer = CompareVisualizer(config)

    if config.dir:
        visualizer.replay_dir()
    else:
        visualizer.replay_file()


if __name__ == '__main__':
    main()

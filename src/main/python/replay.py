#!/usr/bin/env python
import sys
import os

import argparse
from classes.FeaturizedObject import FeaturizedObject
from visualization.visualizer import Visualizer

def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_path", help="the path of the log file or directory", type=str)
    parser.add_argument("--dir", help="the path is a directory or not", action="store_true", default=False)
    parser.add_argument("--image", help="generating images", action="store_true", default=False)
    parser.add_argument("--gif", help="generating gifs", action="store_true", default=False)

    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()
    visualizer = Visualizer(config)

    if config.dir:
        visualizer.replay_dir()
    else:
        visualizer.replay_file()


if __name__ == '__main__':
    main()

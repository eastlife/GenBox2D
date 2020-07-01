#!/usr/bin/env python
import sys
import os

import argparse
from classes.FeaturizedObject import FeaturizedObject
from visualization.visualizer import Visualizer

def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="the path of the log file", type=str)
    parser.add_argument("-i", help="enable the gui mode to replay", action="store_true", default=False)

    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()
    visualizer = Visualizer(config)
    visualizer.draw_single_picture()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import argparse
from classes.Generator import Generator


def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_template_id", help="start template id", type=int)
    parser.add_argument("--end_template_id", help="end template id", type=int)
    parser.add_argument("--num_modifications", help="num_modifications", type=int)
    parser.add_argument("--action_tier", help="action tier <ball/two_balls>")

    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()
    generator = Generator(config)
    action = generator.get_action()
    print("Tasks loaded: ")
    print(generator.tasks)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import argparse
from classes.Generator import Generator
from simulation.box2d_simulator.TaskSimulator import TaskSimulator


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

    print("Tasks loaded: ")
    print(generator.tasks)

    simulator = TaskSimulator()
    for task in generator.tasks:
        print(simulator.add_task(task))
    action = generator.get_action()



if __name__ == '__main__':
    main()

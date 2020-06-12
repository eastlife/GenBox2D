#!/usr/bin/env python
import sys

import time
import argparse
from classes.Generator import Generator


def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_template_id", help="start template id", type=int, default=0)
    parser.add_argument("--end_template_id", help="end template id", type=int, default=0)
    parser.add_argument("--num_modifications", help="num_modifications", type=int, default=1)
    parser.add_argument("--action_tier", help="action tier <ball/two_balls>", default="ball")

    parser.add_argument("--density", help="density of dynamic objects", type=float, default=1.0)
    parser.add_argument("--friction", help="friction of contact objects", type=float, default=0.3)
    parser.add_argument("--restitution", help="restitution of dynamic objects", type=float, default=0.2)

    parser.add_argument("-i", help="enable the interactive/gui mode", action="store_true", default=False)
    parser.add_argument("--task_id", help="input a specific task id with format xxxxx:xxx", type=str)
    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()
    generator = Generator(config)

    print("Tasks loaded: ")
    print(generator.tasks)

    print(sys.argv)
    sys.argv = sys.argv[:1]
    from simulation.box2d_simulator import TaskSimulator
    task = generator.tasks[0]

    simulator = TaskSimulator(task)

    if config.i:
        simulator.run()
    else:
        simulator.run_sim()
    
    
    # for task in generator.tasks:
    #     simulator.add_task(task)
    # action = generator.get_action()
    print("done")



if __name__ == '__main__':
    main()

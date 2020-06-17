#!/usr/bin/env python
import sys
import os

import logging
import time
from datetime import datetime

import argparse
from classes.WorldProperties import WorldProperties
from classes.Generator import Generator


def get_config_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_template_id", help="start template id", type=int, default=0)
    parser.add_argument("--end_template_id", help="end template id", type=int, default=0)
    parser.add_argument("--num_mods", help="number of mods for each template", type=int, default=1)
    parser.add_argument("--action_tier", help="action tier <ball/two_balls>", default="ball")

    parser.add_argument("--config_path", help="name of the config file under the config directory", type=str, default="config.json")
    parser.add_argument("--log_file", help="name of the log file under the log directory", type=str, default="genbox2d.log")

    parser.add_argument("-i", help="enable the interactive/gui mode", action="store_true", default=False)
    parser.add_argument("--task_id", help="input a specific task id with format xxxxx:xxx", type=str)

    parser.add_argument("--frequency", help="frequency for box2d steps", type=int, default=60)
    parser.add_argument("--total_steps", help="total sampling steps", type=int, default=600)
    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()

    logging.basicConfig(filename=config.log_file, filemode='w', format='%(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create directory for log file
    now = datetime.now()

    now_dir = now.strftime("%m-%d-%Y-%H-%M-%S")
    now_dir = "log-" + now_dir
    os.mkdir(now_dir)

    generator = Generator(config)

    config_path_abs = os.path.join(os.getcwd(), "config", config.config_path)

    properties = WorldProperties(config_path_abs)

    print("Tasks loaded: ")
    print(generator.tasks)

    print(sys.argv)
    sys.argv = sys.argv[:1]
    from simulation.box2d_simulator import TaskSimulator

    simulator = TaskSimulator(config, generator.tasks, properties, logger)

    if config.i:
        simulator.run()
    else:
        for i in range(len(generator.tasks)):
            print("**Run task**")
            simulator.run_sim()
            simulator.next_task()
    
    
    # for task in generator.tasks:
    #     simulator.add_task(task)
    # action = generator.get_action()
    print("done")



if __name__ == '__main__':
    main()

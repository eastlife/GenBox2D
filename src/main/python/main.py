#!/usr/bin/env python
import sys
import os
import phyre
import matplotlib.pyplot as plt

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

    parser.add_argument("-i", help="enable the interactive/gui mode", action="store_true", default=False)
    parser.add_argument("--task_id", help="input a specific task id with format xxxxx:xxx", type=str)

    parser.add_argument("--frequency", help="frequency for box2d steps", type=int, default=60)
    parser.add_argument("--total_steps", help="total sampling steps", type=int, default=600)

    parser.add_argument("--always_active", help="set objects in the scene to be active at all times", action="store_true", default=False)

    parser.add_argument("--solved_threshold", help="the minimum frames (steps) for two goal objects contacted", type=int, default=60)

    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()

    generator = Generator(config)

    raw_action, scaled_action = generator.get_single_action()

    # # using PHYRE API to simulate and visualize
    # for i in range(len(generator.simulator.task_ids)):
    #     simulation = generator.simulator.simulate_action(i, raw_action, need_images=True)
    #     image = phyre.observations_to_float_rgb(simulation.images[0])
    #     print(image.shape)

    #     plt.imsave(str(i) + ".png", image)

    print('ids')
    print(generator.simulator.task_ids)

    # actions = generator.get_multiple_actions(10)
    # print('actions')
    # print(actions)

    config_path_abs = os.path.join(os.getcwd(), "config", config.config_path)

    properties = WorldProperties(config_path_abs)

    print("Tasks loaded: ")
    print(generator.tasks)

    print(sys.argv)
    sys.argv = sys.argv[:1]
    from simulation.box2d_simulator import TaskSimulator

    simulator = TaskSimulator(config, generator.tasks, properties, scaled_action)

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

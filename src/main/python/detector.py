#!/usr/bin/env python
import sys
import os

import argparse
from classes.WorldProperties import WorldProperties
from classes.Generator import Generator
from classes.FeaturizedObject import FeaturizedObject
from classes.Task import Task


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
    config = parser.parse_args()
    return config


def main():
    config = get_config_from_args()

    config_path_abs = os.path.join(os.getcwd(), "config", config.config_path)

    properties = WorldProperties(config_path_abs)

    tasks = []
    # shape, color, diameter, initial_x, initial_y, initial_angle

    # Not contacted
    o1 = FeaturizedObject("BALL", "GRAY", 0.1, 0.2, 0.8, 0.0)
    o2 = FeaturizedObject("BALL", "GRAY", 0.1, 0.5, 0.8, 0.0)
    featurized_objects = [o1, o2]

    #task_id, initial_scene, initial_featurized_objects, featurized_objects_wrapper
    new_task = Task("Example:001", None, None, featurized_objects)

    # Contacted
    o3 = FeaturizedObject("BALL", "GRAY", 0.2, 0.3, 0.1, 0.0)
    o4 = FeaturizedObject("BALL", "GRAY", 0.2, 0.4, 0.1, 0.0)
    featurized_objects2 = [o3, o4]

    #task_id, initial_scene, initial_featurized_objects, featurized_objects_wrapper
    new_task2 = Task("Example:002", None, None, featurized_objects2)

    tasks.append(new_task2)
    tasks.append(new_task)


    print("Tasks loaded: ")
    print(tasks)


    print(sys.argv)
    sys.argv = sys.argv[:1]
    from simulation.contact_detector import ContactDetector

    simulator = ContactDetector(config, tasks, properties)

    first_contacts = []
    if config.i:
        simulator.run()
    else:
        for i in range(len(tasks)):
            print("**Run task**")
            first_contact = simulator.run_sim()
            first_contacts.append(first_contact)
            simulator.next_task()
    print("first_contacts")
    print(first_contacts)
    print("done")



if __name__ == '__main__':
    main()

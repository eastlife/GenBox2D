#!/usr/bin/env python
import sys
import os
import phyre
import matplotlib.pyplot as plt
import numpy as np

import argparse
from classes.WorldProperties import WorldProperties
from classes.Generator import Generator
from solver.collision_solver import CollisionSolver

def get_config_from_args():
    parser = argparse.ArgumentParser()
    # select either a single task id by setting --task_id
    # or a range of tasks by setting --start_template_id, --end_template_id and --num_mods
    parser.add_argument("--task_id", help="input a exp_nameific task id with format xxxxx:xxx", type=str)

    parser.add_argument("--start_template_id", help="start template id", type=int, default=1)
    parser.add_argument("--end_template_id", help="end template id", type=int, default=1)
    parser.add_argument("--num_mods", help="number of mods for each template", type=int, default=100)

    # this argument should always be "ball" ("two_balls" is not supported for now)
    parser.add_argument("--action_tier", help="action tier <ball/two_balls>", default="ball")

    parser.add_argument("--config_path", help="name of the config file under the config directory", type=str, default="config.json")

    # actions
    parser.add_argument("--no_actions", help="run tasks without actions (default is different actions)", action="store_true", default=False)
    parser.add_argument("--same_actions", help="run tasks with a unique action for all tasks (default is multdifferentiple actions)", action="store_true", default=False)
    parser.add_argument("--seed", help="random seed to selection actions", type=int, default=1)

    parser.add_argument("-i", help="enable the interactive/gui mode", action="store_true", default=False)

    parser.add_argument("--frequency", help="frequency for box2d steps", type=int, default=60)
    parser.add_argument("--total_steps", help="total sampling steps", type=int, default=600)

    # set always_active to be true if you wants to test the task is solved or not
    parser.add_argument("--always_active", help="set objects in the scene to be active at all times", action="store_true", default=False)

    parser.add_argument("--solved_threshold", help="the minimum frames (steps) for two goal objects contacted", type=int, default=60)
    parser.add_argument("--exp_name", type=str, default='gine')
    config = parser.parse_args()
    return config


#def simulate(sid=1, eid=1, num_mods=100, raw_dataset_name='1-1x100', exp_name='gine', root_dir='/home/yiran/pc_mapping/GenBox2D/src/main/python'):
def simulate(config):

    generator = Generator(config)

    print('ids')
    print(generator.simulator.task_ids)


    #if config.no_actions:
    #    raw_actions, scaled_actions = [], []
    #elif config.same_actions:
    #    raw_actions, scaled_actions = generator.get_same_actions(len(generator.simulator.task_ids))
    #else:
    #    raw_actions, scaled_actions = generator.get_multiple_actions(len(generator.simulator.task_ids))
    #print(root_dir+'/box2d_data/'+raw_dataset_name+'/raw_actions.npy')
    #raw_actions=np.load('/home/yiran/pc_mapping/GenBox2D/src/main/python/box2d_data/1-1x5/raw_actions.npy')
    #scaled_actions=np.load('/home/yiran/pc_mapping/GenBox2D/src/main/python/box2d_data/1-1x5/scaled_actions.npy')
    action_path=config.box2d_root_dir+'/box2d_data/'+config.raw_dataset_name
    raw_actions = np.load(action_path+'/raw_actions.npy')
    scaled_actions=np.load(action_path+'/scaled_actions.npy')
    # # using PHYRE API to simulate and visualize
    # for i in range(len(generator.simulator.task_ids)):
    #     simulation = generator.simulator.simulate_action(i, raw_actions[0], need_images=True)
    #     image = phyre.observations_to_float_rgb(simulation.images[0])
    #     print(image.shape)

    #     plt.imsave(str(i) + ".png", image)


    #config_path_abs = os.path.join(os.getcwd(), "config", config.config_path)
    config_path_abs=os.path.join(config.box2d_root_dir,'config', config.config_path)

    properties = WorldProperties(config_path_abs)

    print("Tasks loaded: ")
    print(generator.tasks)

    print(sys.argv)
    sys.argv = sys.argv[:1]
    os.system('rm -r %s/nn_rollout/%s'%(config.box2d_root_dir, config.exp_name))

    # This import requires GUI
    from simulation.rollout_simulator import RolloutSimulator

    selected_tasks=[]
    selected_actions=[]
    for i in range(config.end_template_id-config.start_template_id+1):
        for j in range(min(3,config.num_mods)):
            selected_tasks.append(generator.tasks[i*config.num_mods+j])
            selected_actions.append(scaled_actions[i*config.num_mods+j])
    forward_model=CollisionSolver()
    #simulator = RolloutSimulator(config, generator.tasks, properties,
    #                             scaled_actions, forward_model, exp_name, root_dir)
    simulator = RolloutSimulator(config, selected_tasks, properties,
                                 selected_actions, forward_model)

    if config.i:
        simulator.run()
    else:
        #for i in range(len(generator.tasks)):
        for i in range(len(selected_tasks)):
            print("**Run task**")
            simulator.run_sim()
            simulator.next_task()

    print("done")


if __name__ == '__main__':
    #config = get_config_from_args()
    simulate(1,1,5)

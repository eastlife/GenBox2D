import phyre
import random
from .Task import Task
from utils.task_reader import load_compiled_task_dict
from phyre import action_mappers

random.seed(0)

'''
A class for Task.
task_id: Each task id consists of a template id and a modification id.
'''
class Generator:
    def __init__(self, config):
        self.start_template_id = config.start_template_id
        self.end_template_id = config.end_template_id
        self.num_mods = config.num_mods
        self.action_tier = config.action_tier
        self.task_id = config.task_id

        self.action_mappers = action_mappers.ACTION_MAPPERS[self.action_tier]()

        tasks_map, _ = load_compiled_task_dict()
        task_ids = []
        if self.task_id is not None:
            task_ids.append(self.task_id)
        else:
            self.template_num = self.end_template_id - self.start_template_id + 1
            for i in range(self.start_template_id, self.end_template_id + 1, 1):
                task_mods = tasks_map[str(i).zfill(5)]
                for j in range(self.num_mods):
                    task_ids.append(str(i).zfill(5) + ":" + task_mods[j])

        # print("tasks: ",)
        # print(task_ids)

        self.simulator = phyre.initialize_simulator(task_ids, self.action_tier)

        self.tasks = []
        for task_index in range(len(task_ids)):
            id = self.simulator.task_ids[task_index]
            initial_scene = self.simulator.initial_scenes[task_index]
            initial_featurized_objects = self.simulator.initial_featurized_objects[task_index]
            task = Task(id, initial_scene, initial_featurized_objects)
            self.tasks.append(task)


    def get_single_action(self, seed=1):
        actions, ball_infos = self.get_multiple_actions(1, max_actions=1, seed=seed)
        return actions[0], ball_infos[0]


    def get_same_actions(self, num, seed=1):
        print("num input: " + str(num))
        actions, ball_infos = self.get_multiple_actions(1, max_actions=1, seed=seed)
        action = actions[0]
        ball_info = ball_infos[0]
        return  [action for i in range(num)],  \
                [ball_info for i in range(num)]

    '''
    NOTICE: PHYRE API does not guarantee actions are always valid!
    '''
    def get_multiple_actions(self, num, max_actions=100, seed=1):
        action_pool = self.simulator.build_discrete_action_space(max_actions=max_actions, seed=seed)

        actions = []
        ball_infos = []
        for i in range(num):
            action = random.choice(action_pool)
            ball_info = self.action_to_ball_info(action)
            actions.append(action)
            ball_infos.append(ball_info)

        return actions, ball_infos


    '''
    returns (x, y, radius) (percentage of SCENE_WIDTH)
    only for one ball tier
    '''
    def action_to_ball_info(self, action):
        SCENE_WIDTH = SCENE_HEIGHT = 256
        # user_input = self.action_mappers.action_to_user_input(action)[0]
        # assume only for tier 'ball' (one ball only) 
        # ball = user_input.balls[0]
        MIN_RADIUS = 2
        MAX_RADIUS = max(SCENE_WIDTH, SCENE_HEIGHT) // 8

        radius = self._scale(action[2], MIN_RADIUS, MAX_RADIUS)

        return (action[0], action[1], radius / 256)
        # return (ball.position.x / PHYRE_WIDTH, ball.position.y / PHYRE_WIDTH, 4 / PHYRE_WIDTH)


    def _scale(self, x, low, high):
        return x * (high - low) + low

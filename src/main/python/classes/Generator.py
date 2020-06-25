import phyre
from .Task import Task
from read_tasks import load_compiled_task_dict
from phyre import action_mappers


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

    '''
    returns (x, y, radius) (percentage of SCENE_WIDTH)
    '''
    def get_single_action(self, valid=True):
        action = self.simulator.sample(valid_only=True, rng=None)
        user_input = self.action_mappers.action_to_user_input(action)[0]
        # assume only for tier 'ball' (one ball only) 
        ball = user_input.balls[0]
        print("action")
        print(ball.position.x) # action * 256 = ball.position.x
        print(ball.position.y) # action * 256 = ball.position.y
        print(ball.radius) # don't know how to get radius from action
        return (action[0], action[1], ball.radius / 256)
    
    def get_multiple_actions(self, num, seed=1):
        return self.simulator.build_discrete_action_space(num, seed=seed)

import phyre
from .Task import Task
from read_tasks import load_compiled_task_dict


'''
A class for Task.
task_id: Each task id consists of a template id and a modification id.
'''
class Generator:
    def __init__(self, config):
        self.start_template_id = config.start_template_id
        self.end_template_id = config.end_template_id
        self.num_modifications = config.num_modifications
        self.action_tier = config.action_tier

        tasks_map, _ = load_compiled_task_dict()
        task_ids = []
        self.template_num = self.end_template_id - self.start_template_id + 1
        for i in range(self.start_template_id, self.end_template_id + 1, 1):
            task_mods = tasks_map[str(i).zfill(5)]
            for j in range(self.num_modifications):
                task_ids.append(str(i).zfill(5) + ":" + task_mods[j])

        # print("tasks: ",)
        # print(task_ids)

        self.simulator = phyre.initialize_simulator(task_ids, self.action_tier)

        self.tasks = []
        for task_index in range(len(task_ids)):
            task_id = self.simulator.task_ids[task_index]
            initial_scene = self.simulator.initial_scenes[task_index]
            initial_featurized_objects = self.simulator.initial_featurized_objects[task_index]
            task = Task(task_id, initial_scene, initial_featurized_objects)
            self.tasks.append(task)

    '''
    returns (task, height, width)
    '''
    def get_action(self, valid=True):
        return self.simulator.sample(valid_only=valid, rng=None)

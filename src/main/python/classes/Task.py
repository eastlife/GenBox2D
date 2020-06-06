import phyre

'''
A class for Task.
task_id: Each task id consists of a template id and a modification id.
'''
class Task:
    def __init__(self, task_id, initial_scene, initial_featurized_objects):
        task = task_id.split(':')
        self.task_id = task_id
        self.template_id = task[0]
        self.modification_id = task[1]
        self.initial_scene = initial_scene
        self.rgb = phyre.observations_to_float_rgb(initial_scene)
        self.initial_featurized_objects = initial_featurized_objects

    def __str__(self):
        return "{ Task: " + self.task_id + " }"

    def __repr__(self):
        return self.__str__()



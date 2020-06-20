import phyre
import json

'''
A class for Task.
task_id: Each task id consists of a template id and a modification id.
'''
class Task:
    def __init__(self, task_id, initial_scene, initial_featurized_objects, featurized_objects_wrapper=None):
        task = task_id.split(':')
        self.task_id = task_id
        self.template_id = task[0]
        self.modification_id = task[1]
        self.initial_scene = initial_scene
        self.rgb = phyre.observations_to_float_rgb(initial_scene)
        self.initial_featurized_objects = initial_featurized_objects

        # Wrapped featurized objects in classes/FeaturizedObject, 
        # only used for creating objects in box2d (with no relation to PHYRE tasks)
        self.featurized_objects_wrapper = featurized_objects_wrapper

    def __str__(self):
        return "{ Task: " + self.task_id + " }"

    def __repr__(self):
        return self.__str__()

    def serialize_task(self):
        json_dict = {}
        json_dict["task_id"] = self.task_id
        
        json_featurized_objects = []
        featurized_objects = self.initial_featurized_objects
        json_dict["num_featurized_objects"] = len(featurized_objects.shapes)
        for i in range(featurized_objects.num_objects):
            json_featurized_object = {}
            json_featurized_object["shape"] = featurized_objects.shapes[i]
            json_featurized_object["color"] = featurized_objects.colors[i]
            json_featurized_object["diameter"] = float(featurized_objects.diameters[i])

            state = featurized_objects.states[0][i]
            json_featurized_object["initial_x"] = float(state[0])
            json_featurized_object["initial_y"] = float(state[1])
            json_featurized_object["initial_angle"] = float(state[2])

            json_featurized_objects.append(json_featurized_object)

        json_dict["featurized_objects"] = json_featurized_objects
        return json.dumps(json_dict)

    def serialize_customized_task(self):
        json_dict = {}
        json_dict["task_id"] = self.task_id
        
        json_featurized_objects = []
        featurized_objects = self.featurized_objects_wrapper
        num_objects = len(self.featurized_objects_wrapper)
        json_dict["num_featurized_objects"] = num_objects
        for i in range(num_objects):
            json_featurized_object = {}
            json_featurized_object["shape"] = featurized_objects[i].shape
            json_featurized_object["color"] = featurized_objects[i].color
            json_featurized_object["diameter"] = float(featurized_objects[i].diameter)

            json_featurized_object["initial_x"] = float(featurized_objects[i].initial_x)
            json_featurized_object["initial_y"] = float(featurized_objects[i].initial_y)
            json_featurized_object["initial_angle"] = float(featurized_objects[i].initial_angle)

            json_featurized_objects.append(json_featurized_object)

        json_dict["featurized_objects"] = json_featurized_objects
        return json.dumps(json_dict)




import phyre
import json
from .FeaturizedObject import FeaturizedObject

'''
A class for Task.
task_id: Each task id consists of a template id and a modification id.
'''
class Task:
    def __init__(self, task_id, initial_scene, phyre_initial_featurized_objects, featurized_objects_wrapper=None):
        task = task_id.split(':')
        self.task_id = task_id
        self.template_id = task[0]
        self.modification_id = task[1]
        self.initial_scene = initial_scene
        self.rgb = phyre.observations_to_float_rgb(initial_scene)

        self.featurized_objects = []

        self.initial_featurized_objects = phyre_initial_featurized_objects
        self.featurized_objects_wrapper = featurized_objects_wrapper

        if self.initial_featurized_objects is not None:
            self._get_featurized_objects_from_phyre()
        if self.featurized_objects_wrapper is not None:
            self._get_featurized_objects_from_wrapper()

        self.goal_objects = []
        self._get_goal_objects()
            
        

        # Wrapped featurized objects in classes/FeaturizedObject, 
        # only used for creating objects in box2d (with no relation to PHYRE tasks)


    def _get_featurized_objects_from_phyre(self):
        for i in range(self.initial_featurized_objects.num_objects):
            shape = self.initial_featurized_objects.shapes[i]
            color = self.initial_featurized_objects.colors[i]
            diameter = self.initial_featurized_objects.diameters[i]
            state = self.initial_featurized_objects.states[0][i]
            x = state[0]
            y = state[1]
            angle = state[2]
            featurized_object = FeaturizedObject(shape, color, diameter, x, y, angle)
            self.featurized_objects.append(featurized_object)

    def _get_featurized_objects_from_wrapper(self):
        for featurized_object in self.featurized_objects_wrapper:
            self.featurized_objects.append(featurized_object)

    def _get_goal_objects(self):
        for featurized_object in self.featurized_objects:
            if featurized_object.is_goal():
                self.goal_objects.append(featurized_object)


    def __str__(self):
        return "{ Task: " + self.task_id + " }"

    def __repr__(self):
        return self.__str__()

    def serialize_task(self):
        json_dict = {}
        json_dict["task_id"] = self.task_id
        
        json_featurized_objects = []
        featurized_objects = self.featurized_objects
        num_objects = len(featurized_objects)
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




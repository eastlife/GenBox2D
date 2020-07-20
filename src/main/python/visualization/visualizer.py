import os

from .object_drawer import draw_scene
from deserializer import deserialize
from classes.FeaturizedObject import FeaturizedObject
from PIL import Image, ImageDraw

from utils.phyre_creator import Constant

class Visualizer:

    def __init__(self, config):
        self.scene_width = Constant.PHYRE_SCENE_WIDTH
        self.scene_height = Constant.PHYRE_SCENE_HEIGHT
        
        self.is_dir = config.dir
        self.generate_image = config.image
        self.generate_gif = config.gif
        self.path = config.log_path


    def deserialize_log(self, path):
        task_info, action_info, timestamp_info, solved_info = deserialize(path)

        self.log_time = solved_info["log_time"]
        self.task_id = task_info["task_id"]

        self.task_info = task_info
        self.action_info = action_info
        self.timestamp_info = timestamp_info
        self.solved_info = solved_info
        self.featurized_objects = self.get_objects_from_json(task_info)
        self.featurized_objects.extend(self.get_objects_from_json(action_info))


    def get_objects_from_json(self, task_info):
        featurized_objects = []
        for featurized_object_json in task_info['featurized_objects']:
            featurized_object = self.get_object_from_json(featurized_object_json)
            featurized_objects.append(featurized_object)
        return featurized_objects


    def get_object_from_json(self, featurized_object_json):
        shape = featurized_object_json['shape']
        color = featurized_object_json['color']
        diameter = featurized_object_json['diameter']
        x = featurized_object_json['initial_x']
        y = featurized_object_json['initial_y']
        angle = featurized_object_json['initial_angle']
        featurized_object = FeaturizedObject(shape, color, diameter, x, y, angle)
        return featurized_object

    def replay_dir(self):
        logs = os.listdir(self.path)
        for log_file in logs:
            print("log file: " + log_file)

            self.replay(self.path + "/" + log_file)
            

    def replay_file(self):
        self.replay(self.path)


    def replay(self, path):
        image_arr=self.draw_pictures(path)

        if self.generate_gif:
            if not os.path.exists("gif"):
                os.mkdir("gif")

            #image_arr[0].save("gif/" + self.log_time + "-" + self.task_id + ".gif", save_all=True, append_images=image_arr)
            image_arr[0].save("gif/" + self.path + "-" + self.task_id + ".gif", save_all=True,
                              append_images=image_arr)


    def draw_single_picture(self, name):
        image = Image.new("RGB", (self.scene_width, self.scene_height), "white")
        draw = ImageDraw.Draw(image)

        draw_scene(draw, self.scene_width, self.scene_height, self.featurized_objects)

        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        if self.generate_image:
            image_path = "images/images-" + self.log_time + "-" + self.task_id
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            
            image.save(image_path + "/" + name + ".jpg")
        return image

    def draw_pictures(self, path):
        self.deserialize_log(path)
        self.draw_single_picture("initial")
        image_arr = []

        timestamp_info = self.timestamp_info

        for timestamp, info in enumerate(timestamp_info):
            featurized_objects = self.featurized_objects
            for idx, body in enumerate(info['body_info']['bodies']):
                featurized_objects[idx].initial_x = (body['pos_x'] + 10) / 20.0
                featurized_objects[idx].initial_y = body['pos_y'] / 20.0
                featurized_objects[idx].initial_angle = body['angle']

            image = self.draw_single_picture(str(timestamp))
            image_arr.append(image)
        return image_arr
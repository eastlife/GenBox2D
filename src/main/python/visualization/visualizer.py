from .object_drawer import draw_scene
from deserializer import deserialize
from classes.FeaturizedObject import FeaturizedObject
from PIL import Image, ImageDraw

class Visualizer:

    def __init__(self, config):
        self.scene_width = 256
        self.scene_height = 256

        path = config.file_path
        task_info, timestamp_info = deserialize(path)
        print(task_info)
        print(timestamp_info[0])
        print(timestamp_info[-1])
        self.task_info = task_info
        self.timestamp_info = timestamp_info
        self.featurized_objects = self.get_objects_from_json(task_info)


    def get_objects_from_json(self, task_info):
        featurized_objects = []
        for featurized_object_json in task_info['featurized_objects']:
            shape = featurized_object_json['shape']
            color = featurized_object_json['color']
            diameter = featurized_object_json['diameter']
            x = featurized_object_json['initial_x']
            y = featurized_object_json['initial_y']
            angle = featurized_object_json['initial_angle']
            featurized_object = FeaturizedObject(shape, color, diameter, x, y, angle)
            featurized_objects.append(featurized_object)
        return featurized_objects


    def replay(self):
        timestamp_info = self.timestamp_info
        self.draw_single_picture("initial")
        for timestamp, info in enumerate(timestamp_info):
            featurized_objects = self.featurized_objects
            for idx, body in enumerate(info['body_info']['bodies']):
                featurized_objects[idx].initial_x = (body['pos_x'] + 10) / 20.0
                featurized_objects[idx].initial_y = body['pos_y'] / 20.0
                featurized_objects[idx].initial_angle = body['angle']
            print(featurized_objects[0].initial_x, featurized_objects[idx].initial_y)
            self.draw_single_picture(str(timestamp))


    def draw_single_picture(self, name):
        image = Image.new("RGB", (self.scene_width, self.scene_height), "white")
        draw = ImageDraw.Draw(image)

        draw_scene(draw, self.scene_width, self.scene_height, self.featurized_objects)

        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save("images/" + name + ".jpg")
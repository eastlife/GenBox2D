from .object_drawer import draw_scene
from deserializer import deserialize
from classes.FeaturizedObject import FeaturizedObject
from PIL import Image, ImageDraw

class Visualizer:

    def __init__(self, config):
        self.scene_width = 256
        self.scene_height = 256

        path = config.file_path
        task_info, action_info, timestamp_info, solved_info = deserialize(path)
        print(task_info)
        print(action_info)
        print(timestamp_info[0])
        print(timestamp_info[-1])
        print(solved_info)
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


    def replay(self):
        timestamp_info = self.timestamp_info
        self.draw_single_picture("initial")
        image_arr = []
        for timestamp, info in enumerate(timestamp_info):
            featurized_objects = self.featurized_objects
            for idx, body in enumerate(info['body_info']['bodies']):
                featurized_objects[idx].initial_x = (body['pos_x'] + 10) / 20.0
                featurized_objects[idx].initial_y = body['pos_y'] / 20.0
                featurized_objects[idx].initial_angle = body['angle']
            # print(featurized_objects[0].initial_x, featurized_objects[idx].initial_y)
            image = self.draw_single_picture(str(timestamp))
            image_arr.append(image)

        image_arr[0].save('images/out.gif', save_all=True, append_images=image_arr)



    def draw_single_picture(self, name):
        image = Image.new("RGB", (self.scene_width, self.scene_height), "white")
        draw = ImageDraw.Draw(image)

        draw_scene(draw, self.scene_width, self.scene_height, self.featurized_objects)

        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save("images/" + name + ".jpg")
        return image

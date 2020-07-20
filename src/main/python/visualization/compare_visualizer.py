import os

from .object_drawer import draw_scene
from deserializer import deserialize
from classes.FeaturizedObject import FeaturizedObject
from PIL import Image, ImageDraw
import numpy as np
import imageio

from utils.phyre_creator import Constant
from .visualizer import Visualizer

class CompareVisualizer(Visualizer):

    def __init__(self, config):
        super(CompareVisualizer, self).__init__(config)
        self.box2d_data_path=config.box2d_data_path+'/'+config.tasks_label
        self.nn_data_path=config.nn_data_path+'/'+config.spec+config.tasks_label

    def replay_dir(self):
        os.system('mkdir gif/%s'%self.path)
        #logs_box2d = os.listdir(self.box2d_data_path)
        logs_nn = os.listdir(self.nn_data_path)
        #for log_box2d, log_nn in zip(logs_box2d, logs_nn):
        #    print("log file: %s   %s"%(log_box2d, log_nn))
        #    self.dual_replay(self.box2d_data_path + "/" + log_box2d, self.nn_data_path + '/' + log_nn)
        for filename in logs_nn:
            print("log file: %s"%filename)
            self.dual_replay(self.box2d_data_path + "/" + filename, self.nn_data_path + '/' + filename)

    def dual_replay(self, path1, path2):
        #print('call compare_visualizer.dual_replay() with %s %s'%(path1, path2))
        box2d_image_arr=self.draw_pictures(path1)
        #print('@compare_visualizer.dual_replay: draw nn image')
        nn_image_arr=self.draw_pictures(path2)
        concat_image_arr = []

        for box2d_image, nn_image in zip(box2d_image_arr, nn_image_arr):
            image=np.concatenate([np.asarray(box2d_image), np.asarray(nn_image)], axis=1)
            concat_image_arr.append(image)
        #exit()
        if self.generate_gif:
            if not os.path.exists("gif"):
                os.mkdir("gif")
            imageio.mimwrite("gif/" + self.path + "/" + self.task_id + ".gif", concat_image_arr)

    '''
    def dual_replay(self, path1, path2):
        box2d_image_arr=self.draw_pictures(path1)
        nn_image_arr=self.draw_pictures(path2)
        concat_image_arr = []

        for box2d_image, nn_image in zip(box2d_image_arr, nn_image_arr):
            image=Image.fromarray(np.concatenate([np.asarray(box2d_image), np.asarray(nn_image)], axis=1))
            concat_image_arr.append(image)
        box2d_image_arr[1].save('gif/' + self.path + "/"+'01.jpg')
        #exit()
        if self.generate_gif:
            if not os.path.exists("gif"):
                os.mkdir("gif")

            # image_arr[0].save("gif/" + self.log_time + "-" + self.task_id + ".gif", save_all=True, append_images=image_arr)
            concat_image_arr[0].save("gif/" + self.path + "/" + self.task_id + ".gif", save_all=True,
                              append_images=concat_image_arr[1:], loop=0, fps=24)
    '''
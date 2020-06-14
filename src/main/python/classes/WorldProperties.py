import sys
import os

import json

class WorldProperties:
    def __init__(self, path):
        with open(path) as f:
            config_dict = json.load(f)
            self.gravity = -10.0
            
            self.general_density = config_dict["general_density"]
            self.ball_density = self.bar_density = self.jar_density = self.standing_stick_density = self.general_density
            self.general_friction = config_dict["general_friction"]
            self.ball_friction = self.bar_friction = self.jar_friction = self.standing_stick_friction = self.general_density
            self.general_restitution = config_dict["general_restitution"]
            self.ball_restitution = self.bar_restitution = self.jar_restitution = self.standing_stick_restitution = self.general_density

            for shape in config_dict["shapes"]:
                if shape["type"] == "ball":
                    self.ball_density = shape["density"]
                    self.ball_friction = shape["friction"]
                    self.ball_restitution = shape["restitution"]
                elif shape["type"] == "bar":
                    self.bar_density = shape["density"]
                    self.bar_friction = shape["friction"]
                    self.bar_restitution = shape["restitution"]
                elif shape["type"] == "jar":
                    self.jar_density = shape["density"]
                    self.jar_friction = shape["friction"]
                    self.jar_restitution = shape["restitution"]
                elif shape["type"] == "standing_stick":
                    self.standing_stick_density = shape["density"]
                    self.standing_stick_friction = shape["friction"]
                    self.standing_stick_restitution = shape["restitution"]

import sys
import os

import json

class WorldProperties:
    def __init__(self, path):
        with open(path) as f:
            config_dict = json.load(f)
            self.gravity = -10.0
            self.shapes = ["ball", "bar", "jar", "standing_stick"]
            
            self.densities = self.frictions = self.restitutions = {}
            self.general_density = config_dict["general_density"]
            self.general_friction = config_dict["general_friction"]
            self.general_restitution = config_dict["general_restitution"]

            for shape in self.shapes:
                self.densities[shape] = config_dict["general_density"]
                self.frictions[shape] = config_dict["general_friction"]
                self.restitutions[shape] = config_dict["general_restitution"]
 
            for shape in config_dict["shapes"]:
                if shape["type"] in self.shapes:
                    self.densities[shape["type"]] = shape["density"]
                    self.frictions[shape["type"]] = shape["friction"]
                    self.restitutions[shape["type"]] = shape["restitution"]
                else:
                    print("Unsupported shape '{shape}' in config file".format(shape = shape["type"]))
                    exit(1)

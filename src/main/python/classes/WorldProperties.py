import sys
import os

import json

class WorldProperties:
    def __init__(self, path):
        with open(path) as f:
            config_dict = json.load(f)
            self.gravity = -10.0
            
            self.densities = self.frictions = self.restitutions = {}
            self.general_density = config_dict["general_density"]
            self.densities["ball"] = self.densities["bar"] = self.densities["jar"] = self.densities["standing_stick"] = self.general_density
            self.general_friction = config_dict["general_friction"]
            self.frictions["ball"] = self.frictions["bar"] = self.frictions["jar"] = self.frictions["standing_stick"] = self.general_density
            self.general_restitution = config_dict["general_restitution"]
            self.restitutions["ball"] = self.restitutions["bar"] = self.restitutions["jar"] = self.restitutions["standing_stick"] = self.general_density

            for shape in config_dict["shapes"]:
                if shape["type"] == "ball" or shape["type"] == "bar" or shape["type"] == "jar" or shape["type"] == "standing_stick":
                    self.densities[shape["type"]] = shape["density"]
                    self.frictions[shape["type"]] = shape["friction"]
                    self.restitutions[shape["type"]] = shape["restitution"]
                else:
                    print("Unsupported shape '{shape}' in config file".format(shape = shape["type"]))
                    exit(1)

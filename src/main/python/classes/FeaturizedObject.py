
'''
A Wrapper for a single featurized object. Only used for creating objects in box2d
'''
class FeaturizedObject:
    def __init__(self, shape, color, diameter, initial_x, initial_y, initial_angle):
        self.shape = shape
        self.color = color
        self.diameter = diameter
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.initial_angle = initial_angle

    def is_goal(self):
        if self.color == "BLUE" or self.color == "PURPLE" or self.color == "GREEN":
            return True
        return False
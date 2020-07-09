import math


class Transform:

    @staticmethod
    def width_percent_to_x(scene_width, width_percent):
        return - scene_width / 2 + width_percent * scene_width

    @staticmethod
    def height_percent_to_y(scene_height, height_percent):
        return height_percent * scene_height

    @staticmethod
    def diameter_percent_to_length(scene_width, diameter_percent):
        return diameter_percent * scene_width

    #finds the straight-line distance between two points
    @staticmethod
    def distance(ax, ay, bx, by):
        return math.sqrt((by - ay)**2 + (bx - ax)**2)

    #rotates point `A` about point `B` by `angle` radians clockwise.
    @staticmethod
    def rotated_about(ax, ay, bx, by, angle):
        radius = Transform.distance(ax,ay,bx,by)
        angle += math.atan2(ay-by, ax-bx)
        return (
            round(bx + radius * math.cos(angle)),
            round(by + radius * math.sin(angle))
        )
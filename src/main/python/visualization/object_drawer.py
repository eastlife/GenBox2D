import math
from PIL import Image, ImageDraw

from utils.phyre_creator import Constant
from utils.transforms import Transform

def draw_scene(draw, scene_width, scene_height, featurized_objects):
    for featurized_object in featurized_objects:
        shape = featurized_object.shape
        color = featurized_object.color
        diameter = featurized_object.diameter
        x = featurized_object.initial_x
        y = featurized_object.initial_y
        angle = featurized_object.initial_angle
        if shape == "BALL":
            draw_ball(draw, scene_width, scene_height, shape, color, diameter, x, y, angle)
        elif shape == "BAR":
            draw_bar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle)
        elif shape == "JAR":
            draw_jar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle)
        else:
            print("NOT IMPLEMENTED")


def draw_ball(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    center = (x * scene_width, y * scene_height)

    radius = diameter * scene_width / 2 
    circle_vertices = (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius
    )
    shape = [(circle_vertices[0], circle_vertices[1]), (circle_vertices[2], circle_vertices[3])]

    draw.ellipse(shape, fill=color)

def draw_bar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    # constant from PHYRE
    BAR_HEIGHT = scene_width * Constant.BAR_HEIGHT_RATIO

    rectangle_center = (x * scene_width, y * scene_height)
    rectangle_width = BAR_HEIGHT
    rectangle_length = scene_width * diameter

    rectangle_vertices = (
        (rectangle_length / 2, rectangle_width / 2),
        (rectangle_length / 2, -rectangle_width / 2),
        (-rectangle_length / 2, -rectangle_width / 2),
        (-rectangle_length / 2, rectangle_width / 2)
    )

    draw_rectangle(draw, scene_width, scene_height, color, 
                rectangle_center[0], rectangle_center[1], 
                rectangle_center[0], rectangle_center[1], 
                angle, rectangle_vertices)


def draw_rectangle(draw, scene_width, scene_height, color, pos_x, pos_y, rotate_x, rotate_y, angle, vertices):
    rectangle_angle = 180.0 / math.pi * angle

    rectangle_vertices = (
        (vertices[0][0] + pos_x, vertices[0][1] + pos_y),
        (vertices[1][0] + pos_x, vertices[1][1] + pos_y),
        (vertices[2][0] + pos_x, vertices[2][1] + pos_y),  
        (vertices[3][0] + pos_x, vertices[3][1] + pos_y)
    )

    rotate_center = (
        rotate_x,
        rotate_y
    )

    rectangle_vertices = [Transform.rotated_about(x, y, rotate_center[0], rotate_center[1], math.radians(rectangle_angle)) for x,y in rectangle_vertices]
    draw.polygon(rectangle_vertices, fill=color)
    
def draw_jar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    # constants from PHYRE
    BASE_RATIO = Constant.JAR_BASE_RATIO
    WIDTH_RATIO = Constant.JAR_WIDTH_RATIO

    jar_height = scene_width * Constant._jar_diameter_to_default_scale(diameter)
    jar_width = jar_height * WIDTH_RATIO
    jar_base_width = jar_width * BASE_RATIO
    jar_thickness = Constant._jar_thickness_from_height(scene_width, jar_height)
    vertices_list, _ = Constant._build_jar_vertices(height=jar_height, width=jar_width, base_width=jar_base_width, thickness=jar_thickness)
    jar_center = (x * scene_width, y * scene_height)
    for rect in vertices_list:
        draw_rectangle(draw, scene_width, scene_height, color, jar_center[0], jar_center[1], x * scene_width, y * scene_height, angle, rect)



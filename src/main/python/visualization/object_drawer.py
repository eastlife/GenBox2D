import math
from PIL import Image, ImageDraw

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
    BAR_HEIGHT = scene_width / 50.0

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

    rectangle_vertices = [rotated_about(x, y, rotate_center[0], rotate_center[1], math.radians(rectangle_angle)) for x,y in rectangle_vertices]
    draw.polygon(rectangle_vertices, fill=color)
    
def draw_jar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    # constants from PHYRE
    BASE_RATIO = 0.8
    WIDTH_RATIO = 1. / 1.2

    jar_height = scene_width * _diameter_to_default_scale(diameter)
    jar_width = jar_height * WIDTH_RATIO
    jar_base_width = jar_width * BASE_RATIO
    jar_thickness = _thickness_from_height(256, jar_height)
    vertices_list, _ = _build_jar_vertices(height=jar_height, width=jar_width, base_width=jar_base_width, thickness=jar_thickness)
    jar_center = (x * scene_width, y * scene_height)
    for rect in vertices_list:
        draw_rectangle(draw, scene_width, scene_height, color, jar_center[0], jar_center[1], x * scene_width, y * scene_height, angle, rect)



'''
Jar builder function by PHYRE
''' 
def _diameter_to_default_scale(diameter):
    # constants from PHYRE
    BASE_RATIO = 0.8
    WIDTH_RATIO = 1. / 1.2
    base_to_width_ratio = (1.0 - BASE_RATIO) / 2.0 + BASE_RATIO
    width_to_height_ratio = base_to_width_ratio * WIDTH_RATIO
    height = math.sqrt((diameter**2) / (1 + (width_to_height_ratio**2)))
    return height


'''
Jar builder function by PHYRE
'''
def _thickness_from_height(scene_width, height):
    thickness = (math.log(height) / math.log(0.3 * scene_width) * scene_width / 50)
    if thickness < 2.0:
        return 2.0
    return thickness


'''
Jar builder function by PHYRE
'''
def _build_jar_vertices(height, width, thickness, base_width):
        # Create box.
        vertices = []
        for i in range(4):
            vx = (1 - 2 * (i in (1, 2))) / 2. * base_width
            vy = (1 - 2 * (i in (2, 3))) / 2. * thickness
            vertices.append((vx, vy))

        # Compute offsets for jar edge coordinates.
        base = (width - base_width) / 2.
        hypotenuse = math.sqrt(height**2 + base**2)
        cos, sin = base / hypotenuse, height / hypotenuse
        x_delta = thickness * sin
        x_delta_top = thickness / sin
        y_delta = thickness * cos

        # Left tilted edge of jar.
        vertices_left = [
            (-width / 2, height - (thickness / 2)),
            ((-base_width / 2), -(thickness / 2)),
            ((-base_width / 2) + x_delta, y_delta - (thickness / 2)),
            ((-width / 2) + x_delta_top, height - (thickness / 2)),
        ]

        # Right tilted edge.
        vertices_right = [
            (width / 2, height - (thickness / 2)),
            ((width / 2) - x_delta_top, height - (thickness / 2)),
            ((base_width / 2) - x_delta, y_delta - (thickness / 2)),
            ((base_width / 2), -(thickness / 2)),
        ]

        phantom_vertices = (vertices_left[0], vertices_left[1],
                            vertices_right[3], vertices_right[0])
   
        return [vertices, vertices_left, vertices_right], phantom_vertices


#finds the straight-line distance between two points
def distance(ax, ay, bx, by):
    return math.sqrt((by - ay)**2 + (bx - ax)**2)

#rotates point `A` about point `B` by `angle` radians clockwise.
def rotated_about(ax, ay, bx, by, angle):
    radius = distance(ax,ay,bx,by)
    angle += math.atan2(ay-by, ax-bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )


def width_percent_to_x(scene_width, width_percent):
    return - scene_width / 2 + width_percent * scene_width

def height_percent_to_y(scene_height, height_percent):
    return height_percent * scene_height

def diameter_percent_to_length(scene_width, diameter_percent):
    return diameter_percent * scene_width
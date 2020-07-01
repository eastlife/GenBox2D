import math
from PIL import Image, ImageDraw

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
            print("NOT IMPLEMENTED")
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

    bar_diameter = diameter
    bar_angle = angle
    bar_x = x
    bar_y = y

    rectangle_center = (bar_x * scene_width, bar_y * scene_height)
    rectangle_width = 2
    rectangle_length = scene_width * bar_diameter
    rectangle_angle = 360 * bar_angle

    rectangle_vertices = (
        (rectangle_center[0] + rectangle_length / 2, rectangle_center[1] + rectangle_width / 2),
        (rectangle_center[0] + rectangle_length / 2, rectangle_center[1] - rectangle_width / 2),
        (rectangle_center[0] - rectangle_length / 2, rectangle_center[1] - rectangle_width / 2),
        (rectangle_center[0] - rectangle_length / 2, rectangle_center[1] + rectangle_width / 2)
    )

    rectangle_vertices = [rotated_about(x, y, rectangle_center[0], rectangle_center[1], math.radians(rectangle_angle)) for x,y in rectangle_vertices]

    draw.polygon(rectangle_vertices, fill=color)

def draw_jar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    b2_pi = 3.1415926
    scaled_diameter = diameter_percent_to_length(scene_width, diameter)
    scaled_literal_offset = 0.02 * scaled_diameter
    scaled_thickness = diameter_percent_to_length(scene_width, 0.005)

    literal_length_adjust = 0.75 * scaled_diameter
    literal_angle = 0.0
    literal_x_adjust = 3 * literal_length_adjust * literal_angle

    bottom_length_adjust = 0.6 * scaled_diameter
    bottom_y_adjust = 0.15 * scaled_diameter

    center_y_adjust = 1.5 * scaled_thickness
    center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y) - center_y_adjust)

    # literal 1 left
    draw_rectangle(draw, scene_width, scene_height, shape, color, diameter, x, y, angle + 0.25 - 0.01, #(b2_pi/2 - literal_angle) * 180 / b2_pi, 
                                    offset = (scaled_diameter / 2, -scaled_diameter / 2))
                                    # offset = (diameter_percent_to_length(scene_width, scaled_literal_offset) - literal_x_adjust, 
                                    # diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)))
    print(scaled_diameter)
    print(scaled_literal_offset)
    print(diameter_percent_to_length(scene_width, scaled_literal_offset))
    print(literal_x_adjust)
    print((diameter_percent_to_length(scene_width, scaled_literal_offset) - literal_x_adjust, 
                                    diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)))

    # literal 2 right
    draw_rectangle(draw, scene_width, scene_height, shape, color, diameter, x, y, angle + 0.25 + 0.01, #(b2_pi/2 + literal_angle) * 180 / b2_pi, 
                                    offset = (scaled_diameter / 2, scaled_diameter / 2))
                                    # offset = (diameter_percent_to_length(scene_width, scaled_literal_offset) + literal_x_adjust, 
                                    # diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)))

    # bottom
    draw_rectangle(draw, scene_width, scene_height, shape, color, diameter, x, y, angle, 
                                    offset = (0, 0))
                                    # offset = (diameter_percent_to_length(scene_width, 0), 
                                    # diameter_percent_to_length(scene_width, 0) - bottom_y_adjust))
    # literal1_shape = b2PolygonShape()
    # literal1_shape.SetAsBox(literal_length_adjust / 2, # hx
    #                         scaled_thickness, # hy
    #                         b2Vec2(diameter_percent_to_length(scene_width, scaled_literal_offset) - literal_x_adjust, 
    #                                 diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)), # offset 
    #                         b2_pi/2 - literal_angle) # angle
    # # literal1_shape.position.set(b2Vec2(0.1, 0.1))
    # literal2_shape = b2PolygonShape()
    # literal2_shape.SetAsBox(literal_length_adjust / 2, 
    #                         scaled_thickness, 
    #                         b2Vec2(diameter_percent_to_length(scene_width, - scaled_literal_offset) + literal_x_adjust, 
    #                                 diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)), 
    #                         b2_pi/2 + literal_angle)
    # # literal1_shape.pos.set(b2Vec2(-0.1, 0.1))
    # bottom_shape = b2PolygonShape()
    # bottom_shape.SetAsBox(bottom_length_adjust / 2, 
    #                         scaled_thickness, 
    #                         b2Vec2(diameter_percent_to_length(scene_width, 0), 
    #                                 diameter_percent_to_length(scene_width, 0) - bottom_y_adjust), 
    #                         0)

def draw_rectangle(draw, scene_width, scene_height, shape, color, diameter, x, y, angle, offset):

    bar_diameter = diameter
    bar_angle = angle
    bar_x = x
    bar_y = y

    rectangle_center = (bar_x * scene_width, bar_y * scene_height)
    rectangle_width = 2
    rectangle_length = scene_width * bar_diameter
    rectangle_angle = 360 * bar_angle

    rectangle_vertices = (
        (rectangle_center[0] + offset[0] + rectangle_length / 2, rectangle_center[1] + offset[1] + rectangle_width / 2),
        (rectangle_center[0] + offset[0] + rectangle_length / 2, rectangle_center[1] + offset[1] - rectangle_width / 2),
        (rectangle_center[0] + offset[0] - rectangle_length / 2, rectangle_center[1] + offset[1] - rectangle_width / 2),
        (rectangle_center[0] + offset[0] - rectangle_length / 2, rectangle_center[1] + offset[1] + rectangle_width / 2)
    )

    rectangle_vertices = [rotated_about(x, y, rectangle_center[0], rectangle_center[1], math.radians(rectangle_angle)) for x,y in rectangle_vertices]

    draw.polygon(rectangle_vertices, fill=color)

def width_percent_to_x(scene_width, width_percent):
    return - scene_width / 2 + width_percent * scene_width

def height_percent_to_y(scene_height, height_percent):
    return height_percent * scene_height

def diameter_percent_to_length(scene_width, diameter_percent):
    return diameter_percent * scene_width

scene_width = 256
scene_height = 256

image = Image.new("RGB", (scene_width, scene_height), "white")
draw = ImageDraw.Draw(image)


draw_jar(draw, scene_width, scene_height, "jar", "red", 0.1, 0.5, 0.5, 0)


image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.show()
# draw_scene(scene_width, scene_height)

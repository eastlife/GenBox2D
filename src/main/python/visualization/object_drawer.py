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


def draw_scene(scene_width, scene_height, featurized_objects):

    image = Image.new("RGB", (scene_width, scene_height), "white")
    draw = ImageDraw.Draw(image)

    for featurized_object in featurized_objects:
        shape = featurized_object.shape
        color = featurized_object.color
        diameter = featurized_object.diameter
        x = featurized_object.initial_x
        y = featurized_object.initial_y
        angle = featurized_object.initial_angle
        if shape == "BALL":
            visualize_ball(draw, scene_width, scene_height, shape, color, diameter, x, y, angle)
        elif shape == "BAR":
            visualize_bar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle)
        else:
            print("NOT IMPLEMENTED")

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.show()


def visualize_ball(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    center = (x * scene_width, y * scene_height)

    radius = diameter * scene_width / 2 
    print(radius)
    circle_vertices = (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius
    )
    shape = [(circle_vertices[0], circle_vertices[1]), (circle_vertices[2], circle_vertices[3])]
    # w, h = 220, 190
    # shape = [(40, 40), (w - 10, h - 10)] 
    draw.ellipse(shape, fill=color)
    print(shape)
    # draw.ellipse(shape, fill="red")

def visualize_bar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):

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


# scene_width = 256
# scene_height = 256

# draw_scene(scene_width, scene_height)

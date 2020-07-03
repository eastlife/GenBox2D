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

    bar_diameter = diameter
    bar_angle = angle
    bar_x = x
    bar_y = y

    rectangle_center = (bar_x * scene_width, bar_y * scene_height)
    rectangle_width = 2
    rectangle_length = scene_width * bar_diameter
    rectangle_angle =  bar_angle * 180.0 / math.pi

    rectangle_vertices = (
        (rectangle_center[0] + rectangle_length / 2, rectangle_center[1] + rectangle_width / 2),
        (rectangle_center[0] + rectangle_length / 2, rectangle_center[1] - rectangle_width / 2),
        (rectangle_center[0] - rectangle_length / 2, rectangle_center[1] - rectangle_width / 2),
        (rectangle_center[0] - rectangle_length / 2, rectangle_center[1] + rectangle_width / 2)
    )

    rectangle_vertices = [rotated_about(x, y, rectangle_center[0], rectangle_center[1], math.radians(rectangle_angle)) for x,y in rectangle_vertices]

    draw.polygon(rectangle_vertices, fill=color)

def draw_jar(draw, scene_width, scene_height, shape, color, diameter, x, y, angle):
    jar_height = 220 * diameter
    jar_width = 160 * diameter
    jar_base_width = 140 * diameter
    jar_thickness = 4
    vertices_list, _ = _build_jar_vertices(height=jar_height, width=jar_width, base_width=jar_base_width, thickness=jar_thickness)
    jar_center = (x * scene_width, y * scene_height - jar_height / 2 + jar_thickness * 2)
    for rect in vertices_list:
        draw_polygon(draw, scene_width, scene_height, "jar", "red", 1.0, jar_center[0], jar_center[1], x * scene_width, y * scene_height, angle, rect)


def draw_polygon(draw, scene_width, scene_height, shape, color, diameter, pos_x, pos_y, rotate_x, rotate_y, angle, vertices):

    # rectangle_center = (x * scene_width, y * scene_height)
    rectangle_width = 2
    rectangle_length = scene_width * diameter
    rectangle_angle = 360 * angle

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

draw_jar(draw, scene_width, scene_height, "jar", "red", 0.5, 0.5, 0.5, 0.25)
draw_jar(draw, scene_width, scene_height, "jar", "red", 0.5, 0.5, 0.5, 0)


image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.show()
# draw_scene(scene_width, scene_height)



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
from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape, b2Vec2,
                   b2Transform, b2Mul, b2BodyDef,
                   b2_pi, b2ContactListener)

import math

def create_body(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle):
    isDynamic = None
    if color == "GRAY":
        # Gray for dynamic objects
        isDynamic = True
    elif color == "GREEN":
        # Green for dynamic balls
        isDynamic = True
    elif color == "BLUE":
        # Blue for dynamic balls
        isDynamic = True
    elif color == "RED":
        # Red for dynamic action balls
        isDynamic = True
    elif color == "BLACK":
        # Black for static objects
        isDynamic = False
    elif color == "PURPLE":
        # Black for static objects
        isDynamic = False

    body = None                                                                                                                                  

    if shape == "BALL":
        body = create_ball(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic)

    elif shape == "BAR":
        body = create_bar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic)

    elif shape == "JAR":
        body = create_jar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic)

    elif shape == "STANDINGSTICKS":
        print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world be missing".format(shape = shape))
    else:
        raise NotImplementedError

    return body

def create_ball(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y))
    radius = diameter_percent_to_length(scene_width, diameter) / 2
    if isDynamic:
        fixture = b2FixtureDef(shape=b2CircleShape(radius=radius),
                                density=properties.densities["ball"], friction=properties.frictions["ball"], restitution=properties.restitutions["ball"])
        body = world.CreateDynamicBody(position=center, fixtures=fixture)
    else:
        body = world.CreateStaticBody(position=center, shapes=b2CircleShape(radius=radius))
    return body

def create_bar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    scaled_thickness = diameter_percent_to_length(scene_width, 0.005)

    theta = b2_pi * 2 * angle
    center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y))
    length = diameter_percent_to_length(scene_width, diameter)
    v1 = (center[0] - length / 2 * math.cos(theta), center[1] - length / 2 * math.sin(theta))
    v2 = (center[0] + length / 2 * math.cos(theta), center[1] + length / 2 * math.sin(theta))
    edge = b2EdgeShape()
    edge.vertices = [v1, v2]
    edge.position = center

    bar_shape = b2PolygonShape(box=(diameter_percent_to_length(scene_width, diameter) / 2, scaled_thickness))
    bar_fixture = b2FixtureDef(shape=bar_shape,
                    density=properties.densities["bar"], friction=properties.frictions["bar"], restitution=properties.restitutions["bar"])

    if isDynamic:
        body = world.CreateDynamicBody(position=center, fixtures=bar_fixture, angle= 2 * b2_pi * angle)
    else:
        body = world.CreateStaticBody(position=center, fixtures=bar_fixture, angle= 2 * b2_pi * angle)
    return body

def create_jar_old(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    # constants
    scaled_diameter = diameter_percent_to_length(scene_width, diameter)
    scaled_literal_offset = 0.02 * scaled_diameter
    scaled_thickness = diameter_percent_to_length(scene_width, 0.005)

    literal_length_adjust = 0.75 * scaled_diameter
    literal_angle = 0.05
    literal_x_adjust = 3 * literal_length_adjust * literal_angle

    bottom_length_adjust = 0.6 * scaled_diameter
    bottom_y_adjust = 0.15 * scaled_diameter

    center_y_adjust = 1.5 * scaled_thickness
    center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y) - center_y_adjust)

    literal1_shape = b2PolygonShape()
    literal1_shape.SetAsBox(literal_length_adjust / 2, # hx
                            scaled_thickness, # hy
                            b2Vec2(diameter_percent_to_length(scene_width, scaled_literal_offset) - literal_x_adjust, 
                                    diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)), # offset 
                            b2_pi/2 - literal_angle) # angle
    # literal1_shape.position.set(b2Vec2(0.1, 0.1))
    literal2_shape = b2PolygonShape()
    literal2_shape.SetAsBox(literal_length_adjust / 2, 
                            scaled_thickness, 
                            b2Vec2(diameter_percent_to_length(scene_width, - scaled_literal_offset) + literal_x_adjust, 
                                    diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)), 
                            b2_pi/2 + literal_angle)
    # literal1_shape.pos.set(b2Vec2(-0.1, 0.1))
    bottom_shape = b2PolygonShape()
    bottom_shape.SetAsBox(bottom_length_adjust / 2, 
                            scaled_thickness, 
                            b2Vec2(diameter_percent_to_length(scene_width, 0), 
                                    diameter_percent_to_length(scene_width, 0) - bottom_y_adjust), 
                            0)

    literal1_fixture = b2FixtureDef(shape=literal1_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])
    literal2_fixture = b2FixtureDef(shape=literal2_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])
    bottom_fixture = b2FixtureDef(shape=bottom_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])

    if isDynamic:
        body = world.CreateDynamicBody(position=center, fixtures=[literal1_fixture, literal2_fixture, bottom_fixture], angle= 2 * b2_pi * angle)
    else:
        body = world.CreateStaticBody(position=center, fixtures=[literal1_fixture, literal2_fixture, bottom_fixture], angle= 2 * b2_pi * angle)

    return body


def create_jar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    BASE_RATIO = 0.8
    WIDTH_RATIO = 1. / 1.2

    jar_height = 20.0 * _diameter_to_default_scale(diameter)
    jar_width = jar_height * WIDTH_RATIO
    jar_base_width = jar_width * BASE_RATIO
    jar_thickness = 16.0 / 256
    vertices_list, _ = _build_jar_vertices(height=jar_height, width=jar_width, base_width=jar_base_width, thickness=jar_thickness)

    jar_center = _get_jar_center(scene_width, scene_height, x, y, angle, jar_height, jar_thickness)

    literal1_shape = b2PolygonShape()
    literal2_shape = b2PolygonShape()
    bottom_shape = b2PolygonShape()

    set_vertices(literal1_shape, vertices_list[0])
    set_vertices(literal2_shape, vertices_list[1])
    set_vertices(bottom_shape, vertices_list[2])

    literal1_fixture = b2FixtureDef(shape=literal1_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])
    literal2_fixture = b2FixtureDef(shape=literal2_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])
    bottom_fixture = b2FixtureDef(shape=bottom_shape,
                        density=properties.densities["jar"], 
                        friction=properties.frictions["jar"], 
                        restitution=properties.restitutions["jar"])

    if isDynamic:
        body = world.CreateDynamicBody(position=jar_center, fixtures=[literal1_fixture, literal2_fixture, bottom_fixture], angle= 2 * b2_pi * angle)
    else:
        body = world.CreateStaticBody(position=jar_center, fixtures=[literal1_fixture, literal2_fixture, bottom_fixture], angle= 2 * b2_pi * angle)
    print("position")
    print(body.position)
    return body


def set_vertices(shape, vertices):
    shape.vertexCount = len(vertices)
    vertices.sort()
    shape.vertices = vertices
    print(shape.vertices)

def _get_jar_center(scene_width, scene_height, x, y, angle, jar_height, jar_thickness):
    return (width_percent_to_x(scene_width, x), 
            height_percent_to_y(scene_height, y) - jar_height * 0.33 * math.cos(2 * math.pi * angle)) # 0.33 is an estimate for the mass center in phyre

'''
Jar builder function by PHYRE
'''
def _diameter_to_default_scale(diameter):
    BASE_RATIO = 0.8
    WIDTH_RATIO = 1. / 1.2
    base_to_width_ratio = (1.0 - BASE_RATIO) / 2.0 + BASE_RATIO
    width_to_height_ratio = base_to_width_ratio * WIDTH_RATIO
    height = math.sqrt((diameter**2) / (1 + (width_to_height_ratio**2)))
    return height

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



def create_standing_sticks(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    pass

def width_percent_to_x(scene_width, width_percent):
    return - scene_width / 2 + width_percent * scene_width

def height_percent_to_y(scene_height, height_percent):
    return height_percent * scene_height

def diameter_percent_to_length(scene_width, diameter_percent):
    return diameter_percent * scene_width
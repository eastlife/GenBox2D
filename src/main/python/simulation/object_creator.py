from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape, b2Vec2,
                   b2Transform, b2Mul, b2BodyDef,
                   b2_pi, b2ContactListener)

from utils.phyre_creator import Constant
from utils.transforms import Transform

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
    center = (
        Transform.width_percent_to_x(scene_width, x), 
        Transform.height_percent_to_y(scene_height, y)
        )
    radius = Transform.diameter_percent_to_length(scene_width, diameter) / 2
    if isDynamic:
        fixture = b2FixtureDef(shape=b2CircleShape(radius=radius),
                                density=properties.densities["ball"], friction=properties.frictions["ball"], restitution=properties.restitutions["ball"])
        body = world.CreateDynamicBody(position=center, fixtures=fixture)
    else:
        body = world.CreateStaticBody(position=center, shapes=b2CircleShape(radius=radius))
    return body

def create_bar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    # constant from PHYRE
    BAR_HEIGHT = scene_width * Constant.BAR_HEIGHT_RATIO

    center = (
        Transform.width_percent_to_x(scene_width, x), 
        Transform.height_percent_to_y(scene_height, y)
        )

    bar_shape = b2PolygonShape(
        box=(Transform.diameter_percent_to_length(scene_width, diameter) / 2, BAR_HEIGHT / 2))
    bar_fixture = b2FixtureDef(shape=bar_shape,
                    density=properties.densities["bar"], friction=properties.frictions["bar"], restitution=properties.restitutions["bar"])

    if isDynamic:
        body = world.CreateDynamicBody(position=center, fixtures=bar_fixture, angle= 2 * b2_pi * angle)
    else:
        body = world.CreateStaticBody(position=center, fixtures=bar_fixture, angle= 2 * b2_pi * angle)
    return body


def create_jar(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    # constants from PHYRE
    BASE_RATIO = Constant.JAR_BASE_RATIO
    WIDTH_RATIO = Constant.JAR_WIDTH_RATIO

    jar_height = scene_width * Constant._jar_diameter_to_default_scale(diameter)
    jar_width = jar_height * WIDTH_RATIO
    jar_base_width = jar_width * BASE_RATIO
    jar_thickness = Constant._jar_thickness_from_height(scene_width, jar_height)
    vertices_list, _ = Constant._build_jar_vertices(height=jar_height, width=jar_width, base_width=jar_base_width, thickness=jar_thickness)

    jar_center = _get_jar_center(scene_width, scene_height, x, y, angle, jar_height, jar_thickness)

    literal1_shape = b2PolygonShape()
    literal2_shape = b2PolygonShape()
    bottom_shape = b2PolygonShape()

    _set_vertices(literal1_shape, vertices_list[0])
    _set_vertices(literal2_shape, vertices_list[1])
    _set_vertices(bottom_shape, vertices_list[2])

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

    return body


def _set_vertices(shape, vertices):
    shape.vertexCount = len(vertices)
    vertices.sort()
    shape.vertices = vertices

def _get_jar_center(scene_width, scene_height, x, y, angle, jar_height, jar_thickness):
    return (
        Transform.width_percent_to_x(scene_width, x), 
        Transform.height_percent_to_y(scene_height, y) - jar_height * 0.33 * math.cos(2 * math.pi * angle)) # 0.33 is an estimate for the mass center in phyre


def create_standing_sticks(world, properties, scene_width, scene_height, shape, color, diameter, x, y, angle, isDynamic):
    pass

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
        center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y))
        radius = diameter_percent_to_length(scene_width, diameter) / 2
        if isDynamic:
            fixture = b2FixtureDef(shape=b2CircleShape(radius=radius),
                                    density=properties.densities["ball"], friction=properties.frictions["ball"], restitution=properties.restitutions["ball"])
            body = world.CreateDynamicBody(position=center, fixtures=fixture)
        else:
            body = world.CreateStaticBody(position=center, shapes=b2CircleShape(radius=radius))

    elif shape == "BAR":
        theta = b2_pi * 2 * angle
        center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y))
        length = diameter_percent_to_length(scene_width, diameter)
        v1 = (center[0] - length / 2 * math.cos(theta), center[1] - length / 2 * math.sin(theta))
        v2 = (center[0] + length / 2 * math.cos(theta), center[1] + length / 2 * math.sin(theta))
        edge = b2EdgeShape()
        edge.vertices = [v1, v2]
        edge.position = center

        if isDynamic:
            bar_shape = b2PolygonShape(box=(diameter_percent_to_length(scene_width, diameter) / 2, diameter_percent_to_length(scene_width, 0.01)))
            bar_fixture = b2FixtureDef(shape=bar_shape,
                            density=properties.densities["bar"], friction=properties.frictions["bar"], restitution=properties.restitutions["bar"])
            body = world.CreateDynamicBody(position=center, fixtures=bar_fixture, angle= 2 * b2_pi * angle)
            print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world will be missing".format(shape = shape))
        else:
            body = world.CreateStaticBody(shapes=edge)

    elif shape == "JAR":
        # constants
        scaled_diameter = diameter_percent_to_length(scene_width, diameter)
        scaled_literal_offset = 0.02 * scaled_diameter
        scaled_thickness = diameter_percent_to_length(scene_width, 0.01)

        literal_angle = 0.075
        literal_x_adjust = 2 * scaled_thickness

        bottom_length_adjust = 0.6 * scaled_diameter
        bottom_y_adjust = 3 * scaled_thickness

        center_y_adjust = 1.5 * scaled_thickness
        center = (width_percent_to_x(scene_width, x), height_percent_to_y(scene_height, y) - center_y_adjust)

        literal1_shape = b2PolygonShape()
        literal1_shape.SetAsBox(diameter_percent_to_length(scene_width, diameter) / 3, # hx
                                scaled_thickness, # hy
                                b2Vec2(diameter_percent_to_length(scene_width, scaled_literal_offset) - literal_x_adjust, 
                                       diameter_percent_to_length(scene_width, scaled_literal_offset * 0.5)), # offset 
                                b2_pi/2 - literal_angle) # angle
        # literal1_shape.position.set(b2Vec2(0.1, 0.1))
        literal2_shape = b2PolygonShape()
        literal2_shape.SetAsBox(diameter_percent_to_length(scene_width, diameter) / 3, 
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
        print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world be missing".format(shape = shape))
    elif shape == "STANDINGSTICKS":
        print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world be missing".format(shape = shape))
    else:
        raise NotImplementedError

    return body


def width_percent_to_x(scene_width, width_percent):
    return - scene_width / 2 + width_percent * scene_width

def height_percent_to_y(scene_height, height_percent):
    return height_percent * scene_height

def diameter_percent_to_length(scene_width, diameter_percent):
    return diameter_percent * scene_width
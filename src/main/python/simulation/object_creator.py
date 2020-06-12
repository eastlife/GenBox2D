from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape, b2Vec2,
                   b2Transform, b2Mul,
                   b2_pi, b2ContactListener)

import math

def create_body(world, shape, color, diameter, x, y, angle):
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

    body = None

    if shape == "BALL":
        if isDynamic:
            fixture = b2FixtureDef(shape=b2CircleShape(radius=diameter_percent_to_length(diameter) / 2),
                                    density=1, friction=0.3, restitution=0.8)
            body = world.CreateDynamicBody(position=(width_percent_to_x(x), height_percent_to_y(y)), fixtures=fixture)
            # body2 = world.CreateDynamicBody(position=(x * SCENE_WIDTH, y * SCENE_HEIGHT), fixtures=fixture)
            # bodies.append(body2)
        else:
            body = world.CreateStaticBody(shapes=b2CircleShape(radius=1.0))
    elif shape == "BAR":
        theta = b2_pi * 2 * angle
        center = (width_percent_to_x(x), height_percent_to_y(y))
        length = diameter_percent_to_length(diameter)
        v1 = (center[0] - length / 2 * math.cos(theta), center[1] - length / 2 * math.sin(theta))
        v2 = (center[0] + length / 2 * math.cos(theta), center[1] + length / 2 * math.sin(theta))
        edge = b2EdgeShape()
        edge.vertices = [v1, v2]
        edge.position = center

        if isDynamic:
            # fixture = b2FixtureDef(shape=edge,
            #                         density=1, friction=0.3, restitution=0.8)
            # body = world.CreateDynamicBody(fixtures=fixture)
            print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world will be missing".format(shape = shape))
        else:
            body = world.CreateStaticBody(shapes=edge)

    elif shape == "JAR":
        print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world be missing".format(shape = shape))
    elif shape == "STANDINGSTICKS":
        print("WARNING! The template includes object type {shape} which is not yet implemented. Some objects in the world be missing".format(shape = shape))
    else:
        raise NotImplementedError

    return body


def width_percent_to_x(width_percent):
    return - self.SCENE_WIDTH / 2 + width_percent * self.SCENE_WIDTH

def height_percent_to_y(height_percent):
    return height_percent * self.SCENE_HEIGHT

def diameter_percent_to_length(diameter_percent):
    return diameter_percent * self.SCENE_WIDTH 
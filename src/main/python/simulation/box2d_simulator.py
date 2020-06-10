from Box2D.examples.framework import (Framework, Keys, main)

from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape,
                   b2Transform, b2Mul,
                   b2_pi)

# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

class TaskSimulator (Framework):
    name = "TwoBallExample"
    description = "A simple example to simulate two balls in the scene and another ball of action."

    def __init__(self):
        super(TaskSimulator, self).__init__()
        self.world.gravity = (0.0, -10.0)

        self.SCENE_WIDTH = 20.0
        self.SCENE_HEIGHT = 20.0

        # The boundaries
        ground = self.world.CreateBody(position=(0, self.SCENE_WIDTH / 2))
        ground.CreateEdgeChain(
            [(-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2)]
        )

        self.task = None
        self.bodies = []

        # fixtures = b2FixtureDef(shape=b2CircleShape(radius=1.0),
        #                         density=1, friction=0.3, restitution=0.5)
        #
        # body = self.world.CreateDynamicBody(
        #     position=(0, 10), fixtures=fixtures)

    def add_task(self, task):
        featurized_objects = task.initial_featurized_objects
        for i in range(featurized_objects.num_objects):
            shape = featurized_objects.shapes[i]
            print("shape: " + shape)
            color = featurized_objects.colors[i]
            print("color: " + color)
            diameter = featurized_objects.diameters[i]
            print("diameter: " + str(diameter))
            state = featurized_objects.states[0][i]
            print("state: ")
            print(state)
            x = state[0]
            y = state[1]
            angle = state[2]

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

            if shape == "BALL":
                if isDynamic:
                    fixture = b2FixtureDef(shape=b2CircleShape(radius=1.0),
                                            density=1, friction=0.3, restitution=0.8)
                    body = self.world.CreateDynamicBody(position=(x * self.SCENE_WIDTH, y * self.SCENE_HEIGHT), fixtures=fixture)
                    self.bodies.append(body)
                else:
                    body = self.world.CreateStaticBody(shapes=b2CircleShape(radius=1.0))
                    self.bodies.append(body)
            elif shape == "BAR":
                pass
            elif shape == "JAR":
                pass
            elif shape == "STANDINGSTICKS":
                pass
            else:
                raise NotImplementedError

        self.task = task

    def Keyboard(self, key):
        if not self.body:
            return

        if key == Keys.K_w:
            pass

    def run(self):
        if self.task is None:
            raise Exception
        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6, 2

        # print inital positions
        self.print_bodies()

        for i in range(600):
            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            self.world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            self.world.ClearForces()
        
            # Now print the position and angle of the body.
            self.print_bodies()

    def print_bodies(self):
        print(len(self.bodies), end =" ")
        for body in self.bodies:
            print(body.position, body.angle, end =" ")
        print()

# if __name__ == "__main__":
#     main(TaskSimulator)
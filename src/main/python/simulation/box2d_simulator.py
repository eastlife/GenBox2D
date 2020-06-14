from Box2D.examples.framework import (Framework, Keys)

from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape,
                   b2Transform, b2Mul,
                   b2_pi, b2ContactListener)

from .object_creator import create_body


class MyListener (b2ContactListener):
    def BeginContact(self, contact):
        # print(contact)
        print("Begin")

    def EndContact(self, contact):
        print("End")

    def PreSolve(self, contact, oldManifold):
        print("PreSolve")

    def PostSolve(self, contact, impulse):
        print("PostSolve")
        print(contact)
        print(impulse)


class TaskSimulator (Framework):
    name = "TwoBallExample"
    description = "A simple example to simulate two balls in the scene and another ball of action."

    def __init__(self, tasks):
        super(TaskSimulator, self).__init__()
        self.world.gravity = (0.0, -10.0)
        self.world.contactListener = MyListener()

        self.SCENE_WIDTH = 20.0
        self.SCENE_HEIGHT = 20.0

        # The boundaries
        ground = self.world.CreateBody(position=(0, self.SCENE_HEIGHT / 2))
        ground.CreateEdgeChain(
            [(-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2)]
        )

        self.bodies = []

        self.tasks = tasks
        self.task_idx = 0
        self.task = None

        self.load_task()


    def load_task(self):
        if self.task_idx >= len(self.tasks) or self.task_idx < 0:
            return False
        self.task = self.tasks[self.task_idx]
        featurized_objects = self.task.initial_featurized_objects
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
            print("angle")
            print(angle)

            body = create_body(self.world, self.SCENE_WIDTH, self.SCENE_HEIGHT, shape, color, diameter, x, y, angle)

            if body is not None:
                self.bodies.append(body)

        print("task loaded")
        print(self.task)

    def next_task(self):
        self.task_idx += 1
        return self.load_task()

    def prev_task(self):
        self.task_idx -= 1
        return self.load_task()

    def replay_task(self):
        return self.load_task()


    def width_percent_to_x(self, width_percent):
        return - self.SCENE_WIDTH / 2 + width_percent * self.SCENE_WIDTH

    def height_percent_to_y(self, height_percent):
        return height_percent * self.SCENE_HEIGHT

    def diameter_percent_to_length(self, diameter_percent):
        return diameter_percent * self.SCENE_WIDTH 


    def run_sim(self):
        if self.task is None:
            raise Exception
        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6, 2

        # print inital positions
        print("init")
        self.print_bodies()

        for i in range(600):
            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            self.world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            self.world.ClearForces()
        
            # Now print the position and angle of the body.
            # self.print_bodies()

    def cleanUp(self):
        if len(self.bodies) == 0:
            return
        for body in self.bodies:
            self.world.DestroyBody(body)
        self.bodies = []


    def Keyboard(self, key):
        isSuccess = True
        if key == Keys.K_c:
            self.cleanUp()
        elif key == Keys.K_RETURN:
            self.cleanUp()
            isSucess = self.next_task()
        elif key == Keys.K_BACKSPACE:
            self.cleanUp()
            isSucess = self.prev_task()
        elif key == Keys.K_r:
            self.cleanUp()
            isSucess = self.replay_task()

    def print_bodies(self):
        print(len(self.bodies), end =" ")
        for body in self.bodies:
            print(body.position, body.angle, end =" ")
        print()

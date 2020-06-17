import json

from Box2D.examples.framework import (Framework, Keys)

from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape,
                   b2Transform, b2Mul,
                   b2_pi, b2ContactListener, b2Contact, b2ContactImpulse)


from .object_creator import create_body


class MyListener (b2ContactListener):
    def __init__(self, bodies, contacts):
        super(MyListener, self).__init__()
        self.bodies = bodies
        self.contacts = contacts

    def BeginContact(self, contact):
        pass

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        # print(contact)
        # print(impulse)
        contact_info = self.log_contact(self.bodies, contact, impulse)
        self.contacts.append(contact_info)
    

    def log_contact(self, bodies, contact, impulse):
        json_contact = {}
        json_contact["body_a"] = find_body(bodies, contact.fixtureA.body)
        json_contact["body_b"] = find_body(bodies, contact.fixtureB.body)
        json_contact["manifold_normal"] = (contact.worldManifold.normal[0], contact.worldManifold.normal[1])

        json_contact["points"] = contact.worldManifold.points

        json_contact["normal_impulse"] = impulse.normalImpulses
        json_contact["tangent_impulse"] = impulse.tangentImpulses
        return json_contact


class TaskSimulator (Framework):
    name = "GenBox2D GUI Tool"
    description = "Visualization for PHYRE tasks."

    def __init__(self, config, tasks, properties, logger):
        super(TaskSimulator, self).__init__()

        self.tasks = tasks
        self.properties = properties
        self.logger = logger

        self.frequency = config.frequency
        self.total_steps = config.total_steps
        self.interactive = config.i

        self.bodies = []
        self.contacts = []

        self.world.gravity = (0.0, properties.gravity)
        self.world.contactListener = MyListener(self.bodies, self.contacts)

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

            body = create_body(self.world, self.properties, self.SCENE_WIDTH, self.SCENE_HEIGHT, shape, color, diameter, x, y, angle)

            if body is not None:
                self.bodies.append(body)

        print("task loaded")
        print(self.task)

    def next_task(self):
        if self.task_idx < len(self.tasks):
            self.task_idx += 1
        return self.load_task()

    def prev_task(self):
        if self.task_idx >= 0:
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
        
        timeStep = 1.0 / self.frequency
        vel_iters, pos_iters = 6, 2

        # print inital positions
        self.logger.info(self.task.serialize_task())

        for i in range(self.total_steps):
            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            self.world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            self.world.ClearForces()
        
            self.logger.info(self.serialize_timestamp(i))
            
            self.contacts.clear()
        self.cleanUp()

    def cleanUp(self):
        if len(self.bodies) == 0:
            return
        for body in self.bodies:
            self.world.DestroyBody(body)
        self.bodies = []
        self.contacts.clear()


    def Keyboard(self, key):
        isSuccess = True
        if key == Keys.K_c:
            self.cleanUp()
        elif key == Keys.K_RETURN:
            self.cleanUp()
            isSuccess = self.next_task()
        elif key == Keys.K_BACKSPACE:
            self.cleanUp()
            isSuccess = self.prev_task()
        elif key == Keys.K_r:
            self.cleanUp()
            isSuccess = self.replay_task()

    def serialize_timestamp(self, timestamp):
        json_dict = {}
        json_dict["timestamp"] = timestamp
        json_dict["body_info"] = self.log_bodies()
        json_dict["contact_info"] = self.log_contacts()
        return json.dumps(json_dict)

    def log_bodies(self):
        json_dict = {}
        json_dict["body_num"] = len(self.bodies)
        json_bodies = []
        for idx, body in enumerate(self.bodies):
            json_body = {}
            json_body["idx"] = idx
            json_body["pos_x"] = body.position[0]
            json_body["pos_y"] = body.position[1]
            json_body["angle"] = body.angle
            json_bodies.append(json_body)

        json_dict["bodies"] = json_bodies
        return json_dict

    def log_contacts(self):
        json_dict = {}
        json_dict["contact_num"] = len(self.contacts)
        json_contacts = []
        for _, contact_info in enumerate(self.contacts):
            json_contacts.append(contact_info)
        json_dict["contacts"] = json_contacts
        return json_dict

def find_body(bodies, body):
    if body in bodies:
        return bodies.index(body)
    else:
        return -1

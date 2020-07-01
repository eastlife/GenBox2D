import os
import json
import logging
from datetime import datetime

from Box2D.examples.framework import (Framework, Keys)

from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape, b2EdgeShape,
                   b2Transform, b2Mul,
                   b2_pi, b2ContactListener, b2Contact, b2ContactImpulse)

from classes.FeaturizedObject import FeaturizedObject

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

    def __init__(self, config, tasks, properties, action):
        super(TaskSimulator, self).__init__()

        self.tasks = tasks
        self.properties = properties

        self.frequency = config.frequency
        self.total_steps = config.total_steps
        self.interactive = config.i
        self.always_active = config.always_active
        self.solved_threshold = config.solved_threshold

        # mutable fields
        self.bodies = []
        self.action_bodies = []
        self.contacts = []
        self.goal_objects = []
        self.max_goal_contact_steps = 0
        self.curr_goal_contact_steps = 0
        self.uniform_action = action

        self.world.gravity = (0.0, properties.gravity)
        self.world.contactListener = MyListener(self.bodies, self.contacts)

        self.SCENE_WIDTH = 20.0
        self.SCENE_HEIGHT = 20.0

        self._create_boundaries()

        self.task_idx = 0
        self.task = None

        self.logger = None
        if not self.interactive:
            # Create logger
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            self.logger = logger

            # Create directory for log file
            now = datetime.now()

            now_dir = now.strftime("%m-%d-%Y-%H-%M-%S")
            now_dir = "log-" + now_dir
            os.mkdir(now_dir)
            self.logging_dir = now_dir

        self.load_task()

    def _create_boundaries(self):
        # The boundaries
        ground = self.world.CreateBody(position=(0, self.SCENE_HEIGHT / 2))
        ground.CreateEdgeChain(
            [(-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, self.SCENE_HEIGHT / 2),
             (self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2),
             (-self.SCENE_WIDTH / 2, -self.SCENE_HEIGHT / 2)]
        )

    def load_task(self):
        if self.task_idx >= len(self.tasks) or self.task_idx < 0:
            return False
        self.task = self.tasks[self.task_idx]

        print("**Loading task: {task_id}**".format(task_id = self.task.task_id))
        for featurized_object in self.task.featurized_objects:
            shape = featurized_object.shape
            print("shape: " + shape)
            color = featurized_object.color
            print("color: " + color)
            diameter = featurized_object.diameter
            print("diameter: " + str(diameter))
            x = featurized_object.initial_x
            y = featurized_object.initial_y
            angle = featurized_object.initial_angle
            print("angle")
            print(angle)

            body = create_body(self.world, self.properties, 
                                self.SCENE_WIDTH, self.SCENE_HEIGHT, 
                                shape, color, diameter, x, y, angle)

            if body is not None:
                self.bodies.append(body)

            if featurized_object.is_goal():
                self.goal_objects.append(body)   
            
        if self.uniform_action is not None:
            self.add_action(self.uniform_action)

        print("**Task {task_id} loaded**".format(task_id = self.task.task_id))

    def add_action(self, action):
        print(action)
        x = action[0]
        y = action[1]
        diameter = action[2] * 2
        shape = "BALL"
        color = "RED"
        angle = 0
        action_object = create_body(self.world, self.properties, 
                                    self.SCENE_WIDTH, self.SCENE_HEIGHT, 
                                    shape, color, diameter, x, y, angle)
        self.bodies.append(action_object)
        featurized_object = FeaturizedObject(shape, color, diameter, x, y, angle)
        self.action_bodies.append(featurized_object)

    def init_action(self, action):
        self.uniform_action = action

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

        if self.logger is not None:
            task_handler = logging.FileHandler(self.logging_dir + '/{task}.log'.format(task = self.task.task_id))
            task_handler.setLevel(logging.INFO)
            self.logger.addHandler(task_handler)

            # log initial positions
            self.logger.info(self.task.serialize_task())
            self.logger.info(self.serialize_action())
        
        timeStep = 1.0 / self.frequency
        vel_iters, pos_iters = 6, 2

        for i in range(self.total_steps):
            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            self.world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            self.world.ClearForces()
        
            if self.logger is not None:
                self.logger.info(self.serialize_timestamp(i))

            self.update_goal_contact()
            self.contacts.clear()

            if self.always_active:
                for body in self.bodies:
                    body.awake = True

        if self.curr_goal_contact_steps > self.max_goal_contact_steps:
            self.max_goal_contact_steps = self.curr_goal_contact_steps

        if self.logger is not None:
            self.logger.info(self.serialize_solved())

        self.cleanUp()

        if self.logger is not None:
            self.logger.removeHandler(task_handler)

    # TODO
    def update_goal_contact(self):
        for contact in self.contacts:
            body_a = self.bodies[contact["body_a"]]
            body_b = self.bodies[contact["body_b"]]
            if body_a in self.goal_objects and body_b in self.goal_objects:
                print(contact)
                self.curr_goal_contact_steps += 1
            else:
                if self.curr_goal_contact_steps > self.max_goal_contact_steps:
                    self.max_goal_contact_steps = self.curr_goal_contact_steps
                self.curr_goal_contact_steps = 0

        
    def is_solved(self):
        return self.max_goal_contact_steps >= self.solved_threshold


    # reset all mutable variables
    def cleanUp(self):
        if len(self.bodies) == 0:
            return
        for body in self.bodies:
            self.world.DestroyBody(body)
        self.curr_goal_contact_steps = 0
        self.max_goal_contact_steps = 0
        self.bodies.clear()
        self.action_bodies.clear()
        self.contacts.clear()
        self.goal_objects.clear()


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

    def serialize_action(self):
        json_dict = {}
        
        json_featurized_objects = []
        featurized_objects = self.action_bodies
        num_objects = len(featurized_objects)
        json_dict["num_action_objects"] = num_objects
        for i in range(num_objects):
            json_featurized_object = {}
            json_featurized_object["shape"] = featurized_objects[i].shape
            json_featurized_object["color"] = featurized_objects[i].color
            json_featurized_object["diameter"] = float(featurized_objects[i].diameter)

            json_featurized_object["initial_x"] = float(featurized_objects[i].initial_x)
            json_featurized_object["initial_y"] = float(featurized_objects[i].initial_y)
            json_featurized_object["initial_angle"] = float(featurized_objects[i].initial_angle)

            json_featurized_objects.append(json_featurized_object)

        json_dict["featurized_objects"] = json_featurized_objects
        return json.dumps(json_dict)


    def serialize_solved(self):
        json_dict = {}
        json_dict["task_id"] = self.task.task_id
        json_dict["is_goal_valid"] = (len(self.goal_objects) == 2)
        json_dict["max_goal_contact_steps"] = self.max_goal_contact_steps
        json_dict["is_solved"] = self.is_solved()
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
            json_body["velocity_x"] = body.linearVelocity[0]
            json_body["velocity_y"] = body.linearVelocity[1]
            json_body["angular_velocity"] = body.angularVelocity
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

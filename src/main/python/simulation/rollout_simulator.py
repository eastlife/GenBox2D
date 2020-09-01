import os
import json
import logging
from .box2d_simulator import Box2DSimulator

class RolloutSimulator(Box2DSimulator):

    def __init__(self, config, tasks, properties, actions, forward_model):
        self.forward_model=forward_model
        super(RolloutSimulator, self).__init__(config, tasks, properties, actions)

    #@override
    def define_loggers(self, config):
        if not self.interactive:
            # Create logger
            logger = logging.getLogger('filelogger')
            logger.setLevel(logging.INFO)
            self.logger = logger

            data_logger=logging.getLogger('datalogger')
            data_logger.setLevel(logging.INFO)
            self.data_logger=data_logger

            # Create directory for log file
            #now_str = "log-" + now_str
            now_str=config.box2d_root_dir + '/' + 'nn_rollout/%s'%config.exp_name
            if not os.path.exists(now_str):
                os.mkdir(now_str)
            self.logging_dir = now_str

    #@override
    def run_sim(self):
        if self.task is None:
            raise Exception

        task_info=self.task.serialize_task()
        action_info=self.serialize_action()
        if self.logger is not None:
            task_handler = logging.FileHandler(self.logging_dir + '/{task}.log'.format(task=self.task.task_id), mode='w')
            task_handler.setLevel(logging.INFO)
            self.logger.addHandler(task_handler)

            # log initial positions
            self.logger.info(task_info)
            self.logger.info(action_info)

        timeStep = 1.0 / self.frequency
        vel_iters, pos_iters = 6, 2
        self.forward_model.update_task(json.loads(task_info), json.loads(action_info))

        for i in range(self.total_steps):
            body_info=self.log_bodies()
            # Instruct the world to perform a single step of simulation. It is
            # generally best to keep the time step and iterations fixed.
            self.world.Step(timeStep, vel_iters, pos_iters)

            # Clear applied body forces. We didn't apply any forces, but you
            # should know about this function.
            self.world.ClearForces()
            contact_info=self.log_contacts()
            new_obj_data, movable_map = self.forward_model(body_info,contact_info)

            self.update_world(new_obj_data, movable_map)

            if self.logger is not None:
                self.logger.info(self.serialize_timestamp(i, body_info, contact_info))

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

    def update_world(self, label, map):
        # angle, px, py, vx, vy, omega
        for i,idx in enumerate(map):
            body_attr=label[i]
            body=self.bodies[idx]
            body._b2Body__SetTransform((body_attr['x'], body_attr['y']), body_attr['theta'])
            #print('@rollout_simulator.update_world: setting velocity ',(body_attr[3], body_attr[4]))
            #assert abs(body_attr[3])<100
            #assert abs(body_attr[4])<100
            #print(body_attr[3])
            #print(body_attr[4])
            body._b2Body__SetLinearVelocity((body_attr['vx'], body_attr['vy']))
            body._b2Body__SetAngularVelocity(body_attr['omega'])


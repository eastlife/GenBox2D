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
            state = featurized_objects.states[0][i]
            print("state: ")
            print(state)


    def Keyboard(self, key):
        if not self.body:
            return

        if key == Keys.K_w:
            pass


if __name__ == "__main__":
    main(TaskSimulator)
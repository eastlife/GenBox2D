from Box2D.examples.framework import (Framework, Keys, main)

from Box2D import (b2FixtureDef, b2PolygonShape, b2CircleShape,
                   b2Transform, b2Mul,
                   b2_pi)


class TwoBallExample (Framework):
    name = "TwoBallExample"
    description = "A simple example to simulate two balls in the scene and another ball of action."

    def __init__(self):
        super(TwoBallExample, self).__init__()
        self.world.gravity = (0.0, -10.0)

        # The boundaries
        ground = self.world.CreateBody(position=(0, 25.6))
        ground.CreateEdgeChain(
            [(-25.6, -25.6),
             (-25.6, 25.6),
             (25.6, 25.6),
             (25.6, -25.6),
             (-25.6, -25.6)]
        )

        fixtures = b2FixtureDef(shape=b2CircleShape(radius=1.0),
                                density=1, friction=0.3, restitution=0.5)

        body = self.world.CreateDynamicBody(
            position=(0, 10), fixtures=fixtures)


    def Keyboard(self, key):
        if not self.body:
            return

        if key == Keys.K_w:
            pass


if __name__ == "__main__":
    main(TwoBallExample)
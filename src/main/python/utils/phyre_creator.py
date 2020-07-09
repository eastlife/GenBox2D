import math


class Constant:
    PHYRE_SCENE_WIDTH = 256
    PHYRE_SCENE_HEIGHT = 256

    # Bar constants
    BAR_HEIGHT_RATIO = 1.0 / 50.0


    # Jar constants
    JAR_BASE_RATIO = 0.8
    JAR_WIDTH_RATIO = 1. / 1.2


    # Jar methods
        
    '''
    Jar builder function by PHYRE
    '''
    @staticmethod
    def _build_jar_vertices(height, width, thickness, base_width):
        # Create box.
        vertices = []
        for i in range(4):
            vx = (1 - 2 * (i in (1, 2))) / 2. * base_width
            vy = (1 - 2 * (i in (2, 3))) / 2. * thickness
            vertices.append((vx, vy))

        # Compute offsets for jar edge coordinates.
        base = (width - base_width) / 2.
        hypotenuse = math.sqrt(height**2 + base**2)
        cos, sin = base / hypotenuse, height / hypotenuse
        x_delta = thickness * sin
        x_delta_top = thickness / sin
        y_delta = thickness * cos

        # Left tilted edge of jar.
        vertices_left = [
            (-width / 2, height - (thickness / 2)),
            ((-base_width / 2), -(thickness / 2)),
            ((-base_width / 2) + x_delta, y_delta - (thickness / 2)),
            ((-width / 2) + x_delta_top, height - (thickness / 2)),
        ]

        # Right tilted edge.
        vertices_right = [
            (width / 2, height - (thickness / 2)),
            ((width / 2) - x_delta_top, height - (thickness / 2)),
            ((base_width / 2) - x_delta, y_delta - (thickness / 2)),
            ((base_width / 2), -(thickness / 2)),
        ]

        phantom_vertices = (vertices_left[0], vertices_left[1],
                            vertices_right[3], vertices_right[0])
   
        return [vertices, vertices_left, vertices_right], phantom_vertices

    
    '''
    Jar builder function by PHYRE
    '''
    @staticmethod
    def _jar_diameter_to_default_scale(diameter):
        base_to_width_ratio = (1.0 - Constant.JAR_BASE_RATIO) / 2.0 + Constant.JAR_BASE_RATIO
        width_to_height_ratio = base_to_width_ratio * Constant.JAR_WIDTH_RATIO
        height = math.sqrt((diameter**2) / (1 + (width_to_height_ratio**2)))
        return height

    '''
    Jar builder function by PHYRE
    '''
    @staticmethod
    def _jar_thickness_from_height(scene_width, height):
        return (math.log(height) / math.log(0.3 * scene_width) * scene_width / 50)

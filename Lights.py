from MathFake import MathFake as mf

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * mf.dot(normal, direction)
    reflect = mf.multiply_matrixs([normal, direction])
    reflect = mf.subtract_V3(reflect, direction)


def refractVector(normal, direction, ior):
    pass



class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = mf.divition(direction, mf.norm(direction))
        self.intensity = intensity
        self.color = color
        self.light_type = DIR_LIGHT

class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.light_type = AMBIENT_LIGHT
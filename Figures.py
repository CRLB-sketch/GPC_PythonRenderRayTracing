from re import U
from MathFake import MathFake as mf

from math import atan2 as arctan2
from math import acos as arccos

from collections import namedtuple
V3 = namedtuple('Point3', ['x', 'y', 'z'])

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, scene_obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.scene_obj = scene_obj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, texture = None, mat_type = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.mat_type = mat_type

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin : list, dir : list):
        L = mf.subtract_V3(self.center, V3(origin[0], origin[1], origin[2]))
        tca = mf.dot(L, dir)        
        d = (mf.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1            
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = mf.add(origin, mf.multiply_matrix_by_a_value(dir, t0))
        normal = mf.subtract_V3(V3(P[0], P[1], P[2]), self.center)
        normal = mf.divition(normal, mf.norm(normal))        

        u = 1 - ((arctan2(normal[2], normal[0]) / (2 * mf.pi())) + 0.5)
        v = arccos(-normal[1]) / mf.pi()

        uvs = (u, v)

        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texcoords = uvs,
                         scene_obj = self)
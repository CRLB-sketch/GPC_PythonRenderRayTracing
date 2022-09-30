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

class Plane(object):
    def __init__(self, position, normal, material) -> None:
        self.position = position        
        self.normal = mf.divition(normal, mf.norm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = mf.dot(dir, self.normal)

        # Distancia = (( planePos - origRayo) ° normal) / (direccionRayo ° normal)
        # Es paralelo cuando el rayo es perpendicular con la normal

        if abs(denom) > 0.0001:
            num = mf.dot(mf.subtract_arrays(self.position, orig), self.normal)
            t = num / denom
            
            if t > 0:
                # Punto de contacto : P = O + t0 * D
                P = mf.add(orig, mf.multiply_matrix_by_a_value(dir, t))
                return Intersect(
                    distance=t,
                    point= P,
                    normal= self.normal,
                    texcoords=None,
                    scene_obj=self
                )

        return None # No habrá contacto

class Disk(object):

    def __init__(self, position, normal, material, radius) -> None:
        self.plane = Plane(position, normal , material)
        self.material = material
        self.radius = radius

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)

        if intersect is None: return None

        # contact_distance = intersect.point - self.plane.position
        contact = mf.subtract_arrays(intersect.point, self.plane.position)
        concact = mf.norm(contact)

        if contact <= self.radius: return None
                
        return Intersect(distance = intersect.distance, point = intersect.point, normal = self.plane.normal, texcoords = None, scene_obj = self)

class AABB(object):
    # Axis Aligned Bounding Box

    def __init__(self, position, size, material) -> None:
        self.position = position
        self.size = size
        self.material = material

        self.planes = []

        half_sizes = [
            size[0] / 2,
            size[1] / 2,
            size[2] / 2
        ]
        # half_size_x = size[0] / 2
        # half_size_y = size[1] / 2
        # half_size_z = size[2] / 2

        # Sides
        self.planes.append(Plane( 
            mf.add(position, [half_sizes[0], 0, 0]),
            (1, 0, 0),
            material
        ))
        self.planes.append(Plane( 
            mf.add(position, [-half_sizes[0], 0, 0]),
            (-1, 0, 0),
            material
        ))

        # Up and Down
        self.planes.append(Plane( 
            mf.add(position, [0, half_sizes[1], 0]),
            (0, 1, 0),
            material
        ))
        self.planes.append(Plane( 
            mf.add(position, [0, -half_sizes[1], 0]),
            (0, -1, 0),
            material
        ))

        # Front and back
        self.planes.append(Plane( 
            mf.add(position, [0, 0, half_sizes[2]]),
            (0, 0, 1),
            material
        ))
        self.planes.append(Plane( 
            mf.add(position, [0, 0, -half_sizes[2]]),
            (0, 0, -1),
            material
        ))

        self.bounds_min = [0, 0, 0]
        self.bounds_max = [0, 0, 0]

        epsilon = 0.001

        for i in range(3):
            self.bounds_min[i] = self.position[i] - (epsilon + half_sizes[i])
            self.bounds_max[i] = self.position[i] + (epsilon + half_sizes[i])

    def ray_intersect(self, orig, dist):
        intersect = None
        t = float('inf')

        for plane in self.planes:
            plane_inter = plane.ray_intersect(orig, dist)
            if plane_inter is not None:
                plane_point = plane_inter.point

                if self.bounds_min[0] <= plane_point[0] <= self.bounds_max[0]:
                    if self.bounds_min[1] <= plane_point[1] <= self.bounds_max[1]:
                        if self.bounds_min[2] <= plane_point[2] <= self.bounds_max[2]:

                            if plane_inter.distance < t:
                                t = plane_inter.distance
                                intersect = plane_inter

                                # Tex corrds

                                u, v = 0, 0

                                # Las uvs de las caras de los lados
                                if plane.normal[0] > 0:
                                    # Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (plane_inter.point[1] - self.bounds_min[1]) / self.size[1]
                                    v = (plane_inter.point[2] - self.bounds_min[2]) / self.size[2]

                                elif abs(plane.normal[1] > 0):
                                    # Mapear uvs para el eje y, usando las coordenadas de X y Z
                                    u = (plane_inter.point[0] - self.bounds_min[0]) / self.size[0]
                                    v = (plane_inter.point[2] - self.bounds_min[2]) / self.size[2]

                                elif abs(plane.normal[1] > 0):
                                    u = (plane_inter.point[0] - self.bounds_min[0]) / self.size[0]
                                    v = (plane_inter.point[1] - self.bounds_min[1]) / self.size[1]

        if intersect is None: return None

        return Intersect(
                    distance=t,
                    point= intersect.point,
                    normal= intersect.normal,
                    texcoords=None,
                    scene_obj=self
                )



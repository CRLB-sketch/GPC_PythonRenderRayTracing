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
        
        # P = O + t0 * D [or] P = O + D * t0
        P = mf.add(origin, mf.multiply_matrix_by_a_value(dir, t0))
        normal = mf.subtract_V3(V3(P[0], P[1], P[2]), self.center)
        normal = mf.divition(normal, mf.norm(normal))        

        u = 1 - ((arctan2(normal[2], normal[0]) / (2 * mf.pi())) + 0.5)
        v = arccos(-normal[1]) / mf.pi()

        uvs = (u, v)

        return Intersect(
            distance = t0,
            point = P,
            normal = normal,
            texcoords = uvs,
            scene_obj = self
        )

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

        contact = mf.subtract_arrays(intersect.point, self.plane.position)
        contact = mf.norm(contact) # Acá saca la magnitud del contact

        if contact <= self.radius: return None
                
        return Intersect(
            distance = intersect.distance, 
            point = intersect.point, 
            normal = self.plane.normal, 
            texcoords = None, 
            scene_obj = self
        )

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

        # Sides
        self.planes.append(Plane( mf.add(position, [half_sizes[0], 0, 0]), (1, 0, 0), material ))
        self.planes.append(Plane( mf.add(position, [-half_sizes[0], 0, 0]), (-1, 0, 0), material ))

        # Up and Down
        self.planes.append(Plane( mf.add(position, [0, half_sizes[1], 0]), (0, 1, 0), material ))
        self.planes.append(Plane( mf.add(position, [0, -half_sizes[1], 0]), (0, -1, 0), material ))

        # Front and back
        self.planes.append(Plane( mf.add(position, [0, 0, half_sizes[2]]), (0, 0, 1), material))
        self.planes.append(Plane( mf.add(position, [0, 0, -half_sizes[2]]), (0, 0, -1), material))

        # Bounds
        self.bounds_min = [0, 0, 0]
        self.bounds_max = [0, 0, 0]

        for i in range(3):
            self.bounds_min[i] = self.position[i] - (mf.epsilon() + half_sizes[i])
            self.bounds_max[i] = self.position[i] + (mf.epsilon() + half_sizes[i])

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
            texcoords=(u, v),
            scene_obj=self
        )

class Triangle(object):

    def __init__(self, A : V3, B: V3, C : V3, material) -> None:
        self.v0 = A
        self.v1 = B
        self.v2 = C        
        self.material = material

    def ray_intersect(self, origin : list, dir : list):
        # Encontrar t y p
        v0v1 = mf.subtract_V3(self.v1, self.v0)        
        v0v2 = mf.subtract_V3(self.v2, self.v0)
        
        normal = mf.cross(v0v1, v0v2)        
        
        position = [
            (self.v0.x + self.v1.x + self.v2.x) / 3,
            (self.v0.y + self.v1.y + self.v2.y) / 3,
            (self.v0.z + self.v1.z + self.v2.z) / 3,
        ]
        
        plane = Plane(position, normal, self.material)
        
        intersect = plane.ray_intersect(origin, dir)
        
        if intersect == None: return None        
         
        u, v, w = 0 , 0 , 0
                        
        edge_0 = (self.v1.y - self.v2.y) * (intersect.point[0] - self.v2.x) + (self.v2.x - self.v1.x) * (intersect.point[1] - self.v2.y)
        edge_1 = (self.v2.y - self.v0.y) * (intersect.point[0] - self.v2.x) + (self.v0.x - self.v2.x) * (intersect.point[1] - self.v2.y)
        edge_2 = (self.v1.y - self.v2.y) * (self.v0.x - self.v2.x) + (self.v2.x - self.v1.x) * (self.v0.y - self.v2.y)
            
        u = edge_0 / edge_2
        v = edge_1 / edge_2
        w = 1 - u - v
                
        if 0 <= u and 0 <= v and 0 <= w:
            return Intersect(
                distance = intersect.distance,
                point = intersect.point,
                normal = normal,
                texcoords = (u, v),
                scene_obj = self
            )
        
        return None

class Torus(object):

    def __init__(self, position, radius_minus, radius_major, material) -> None:
        self.position = position
        self.radius_minus = radius_minus # r # B
        self.radius_major = radius_major # R # A

        self.material = material

    def ray_intersect(self, origin, dir):
        # representar el circulo = (radius_major - radius_minus) / 2
        # retornar la t más cercana del torus
        # t0 = 0

        # Polinomio a la cuarta
        
        # r(t) = o + d * t # Punto de contacto
        # p = mf.add(origin, mf.multiply_matrix_by_a_value(dir, t0))
        # F(r(t)) = 0, t > 0        
        # rx = ox + dx * t
        # ry = oy + dy * t
        # rz = oz + dz * t

        return None

from collections import namedtuple

from MathFake import MathFake as mf
V3 = namedtuple('Point3', ['x', 'y', 'z'])

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * mf.dot(normal, direction)
    reflect = mf.multiply_matrix_by_a_value(normal, reflect)
    reflect = mf.subtract_arrays(reflect, direction)
    reflect = mf.divition(reflect, mf.norm(reflect))
    return reflect

def refractVector(normal, direction, ior):
    pass

# ! Cuando haga funcionar todo esto voy a crear una "clase padre/interface" "LIGHT"
class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = mf.divition(direction, mf.norm(direction))
        self.intensity = intensity
        self.color = color
        self.light_type = DIR_LIGHT

    def get_diffuse_color(self, intersect, raytracer):
        light_dir = mf.multiply_matrix_by_a_value(self.direction, -1)
        intensity = mf.dot(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [
            intensity * self.color[0],
            intensity * self.color[1],
            intensity * self.color[2]
        ]

        return diffuseColor

    def get_spec_color(self, intersect, raytracer):
        light_dir = mf.multiply_matrix_by_a_value(self.direction, -1)
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = mf.subtract_V3(raytracer.cam_position, V3(intersect.point[0], intersect.point[1], intersect.point[2]))
        view_dir = mf.divition(view_dir, mf.norm(view_dir))

        spec_intensity = self.intensity * max(0, mf.dot(view_dir, reflect)) ** intersect.scene_obj.material.spec
        specColor = [
            spec_intensity * self.color[0],
            spec_intensity * self.color[1],
            spec_intensity * self.color[2]
        ]

        return specColor

    def get_shadow_intensity(self, intersect, raytracer):
        light_dir = mf.multiply_matrix_by_a_value(self.direction, -1)

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.scene_obj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


# class PointLight(object):
#     def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
#         self.point = point
#         self.constant = constant
#         self.linear = linear
#         self.quad = quad
#         self.color = color
#         self.lightType = POINT_LIGHT

#     def getDiffuseColor(self, intersect, raytracer):
#         light_dir = np.subtract(self.point, intersect.point)
#         light_dir = light_dir / np.linalg.norm(light_dir)

#         # att = 1 / (Kc + Kl * d + Kq * d * d)
#         #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
#         #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
#         attenuation = 1.0
#         intensity = mf.dot(intersect.normal, light_dir) * attenuation
        
#         intensity = float(max(0, intensity))            
                                                        
#         diffuseColor = [
#             intensity * self.color[0],
#             intensity * self.color[1],
#             intensity * self.color[2]
#         ]

#         return diffuseColor

#     def getSpecColor(self, intersect, raytracer):
#         light_dir = np.subtract(self.point, intersect.point)
#         light_dir = light_dir / np.linalg.norm(light_dir)

#         reflect = reflectVector(intersect.normal, light_dir)

#         view_dir = np.subtract( raytracer.camPosition, intersect.point)
#         view_dir = view_dir / np.linalg.norm(view_dir)

#         # att = 1 / (Kc + Kl * d + Kq * d * d)
#         #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
#         #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
#         attenuation = 1.0

#         spec_intensity = attenuation * max(0,np.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
#         specColor = [
#             spec_intensity * self.color[0],
#             spec_intensity * self.color[1],
#             spec_intensity * self.color[2]
#         ]

#         return specColor

#     def getShadowIntensity(self, intersect, raytracer):
#         light_dir = np.subtract(self.point, intersect.point)
#         light_dir = light_dir / np.linalg.norm(light_dir)

#         shadow_intensity = 0
#         shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
#         if shadow_intersect:
#             shadow_intensity = 1

#         return shadow_intensity

class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.light_type = AMBIENT_LIGHT
        
    def get_diffuse_color(self, intersect, raytracer):
        return mf.multiply_matrix_by_a_value(self.color, self.intensity)
    
    def get_spec_color(self, intersect, raytracer):
        return [0, 0, 0]
    
    def get_shadow_intensity(self, intersect, raytracer):
        return 0
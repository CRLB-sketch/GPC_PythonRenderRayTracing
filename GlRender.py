########################################################################################
"""
    Universidad del Valle de Guatemala
    Graficas por Computadora
    Python Render3D
"""
__author__ = "Cristian Laynez 201281"
__status__ = "Student of Computer Science"

# ! GL Render : Clase donde esta todo el Gl personalizado
# Referencias de Carlos Alonso proporcionado en clase
######################################################################################

import struct
from collections import namedtuple

from math import cos, sin, tan, pi
from turtle import width

from Obj import Obj
from Texture import Texture

from MathFake import MathFake as mf

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def color(r : int, g : int, b : int): return bytes([int(b * 255), int(g * 255), int(r * 255)])

def bary_coords(A, B, C, P) -> list:
    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    
    return u, v, w

class Raytracer(object):
    def __init__(self, width : int, height : int):
        self.__gl_init(width, height)
    
    def __gl_init(self, width : int, height : int) -> None:
        self.__gl_create_window(width, height) 
        self.clear_color = color(0, 0, 0)
        self.current_color = color(1, 1, 1)   
        
        self.fov = 60
        self.near_plane = 0.1
        self.cam_position = V3(0, 0, 0)                
        
        self.scene = []
        self.lights = []                
        
        self.gl_clear()             

    def __gl_create_window(self, width : int, height : int) -> None:
        self.width = width
        self.height = height
        self.gl_view_port(0, 0, self.width, self.height)

    def gl_view_port(self, pos_x : int, pos_y : int, width : int, height : int) -> None:
        self.vp_x = pos_x
        self.vp_y = pos_y
        self.vp_width = width
        self.vp_height = height

    def gl_clear_color(self, r : int, g : int, b : int) -> None: self.clear_color = color(r, g, b)

    def gl_color(self, r : int, g : int, b : int) -> None: self.current_color = color(r,g,b)

    def gl_clear(self) -> None:
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

    def gl_clear_viewport(self, clr = None) -> None:
        for x in range(self.vp_x, self.vp_x + self.vp_width):
            for y in range(self.vp_y, self.vp_y + self.vp_height):
                self.gl_point(x, y, clr)

    def gl_point(self, x : int, y : int, clr = None) -> None:
        if ( 0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.current_color
               
    def scene_intersect(self, origin, dir, scene_obj):
        depth = float('inf')
        intersect = None
        
        for obj in self.scene:
            hit = obj.ray_intersect(origin, dir)
            if hit != None:
                if scene_obj != hit.scene_obj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance
                    
        return intersect
    
    def cast_ray(self, origin, dir) -> list:
        intersect = self.scene_intersect(origin, dir, None)
        
        if intersect == None:
            return None
        
        material = intersect.scene_obj.material
        
        final_color = [0, 0, 0]
        object_color = [material.diffuse[0], material.diffuse[1], material.diffuse[2]]
        
        dir_light_color = [0, 0, 0]
        amb_light_color = [0, 0, 0]
        
        for light in self.lights:
            if light.light_type == 0:
                diffuse_color = [0, 0, 0]
                
                light_dir = mf.multiply_matrix_by_a_value(light.direction, -1)
                intensity = mf.dot(intersect.normal, light_dir)
                intensity = float(max(0, intensity))
                
                diffuse_color = [
                    intensity * light.color[0] * light.intensity,
                    intensity * light.color[1] * light.intensity,
                    intensity * light.color[2] * light.intensity,
                ]
                
                # Sombras
                shadow_intensity = 0
                shadow_intersect = self.scene_intersect(intersect.point, light_dir, intersect.scene_obj)
                if shadow_intersect:
                    shadow_intensity = 1
                    
                value_multi_diffuse_by_shadow = mf.multiply_matrix_by_a_value(diffuse_color, (1 - shadow_intensity))
                dir_light_color = mf.add(dir_light_color, value_multi_diffuse_by_shadow)
                
            elif light.light_type == 2:
                amb_light_color = mf.multiply_matrix_by_a_value(light.color, light.intensity)
                
        final_color = mf.add(dir_light_color, amb_light_color)
        
        final_color = mf.multiply_two_lists_or_arrays(final_color, object_color)
        
        r = min(1, final_color[0])
        g = min(1, final_color[1])
        b = min(1, final_color[2])
        
        return (r, g, b)
    
    def gl_render(self) -> None:
        for y in range(self.vp_y, self.vp_y + self.vp_height + 1):
            for x in range(self.vp_x, self.vp_x + self.vp_width + 1):
                # Pasar de coordenadas de ventana a coordenadas NDC (-1 a 1)
                p_x = ((x + 0.5 - self.vp_x) / self.vp_width) * 2 - 1
                p_y = ((y + 0.5 - self.vp_y) / self.vp_height) * 2 - 1
                
                # Proyeccion
                t = tan((self.fov * 3.14159265358979323 / 180) / 2) * self.near_plane
                r = t * self.vp_width / self.vp_height
                
                p_x *= r
                p_y *= t
                
                direction = V3(p_x, p_y, -self.near_plane)
                temp_list_direction = [direction.x, direction.y, direction.z]
                direction = mf.divition(temp_list_direction, mf.norm(temp_list_direction))
                
                ray_color = self.cast_ray(self.cam_position, direction)
                
                if ray_color is not None:
                    ray_color = color(ray_color[0], ray_color[1], ray_color[2])
                    self.gl_point(x, y, ray_color)
               
    def gl_finish(self, filename : str) -> None:
        word = lambda w : struct.pack('=h', w)
        dword = lambda d : struct.pack('=l', d)
        
        with open(filename, "wb") as file:
            #Header
            pixel = dword( 14 + 40 + (self.width * self.height * 3 )) # Multplicado por 3 porque cada pixel tiene 3 bytes
            header = [bytes('B'.encode('ascii')), bytes('M'.encode('ascii')), pixel, dword(0), dword(14 + 40)]
            for e_header in header: file.write(e_header)
    
            # Info Header
            info_header = [
                dword(40), dword(self.width), dword(self.height), word(1), word(24), dword(0), 
                dword(self.width * self.height * 3), dword(0), dword(0), dword(0), dword(0)
            ]
            for e_info_header in info_header: file.write(e_info_header)
            
            # Pintar toda la tabla
            for y in range(self.height):
                for x in range(self.width):                
                    file.write(self.pixels[x][y])

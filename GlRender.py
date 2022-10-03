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
from Figures import *
from Lights import *

from MathFake import MathFake as mf

STEPS = 1
MAX_RECURSION_DEPTH = 4

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

        self.env_map = None
             
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
    
    def cast_ray(self, origin, dir, scene_obj = None, recursion = 0) -> list:
        intersect = self.scene_intersect(origin, dir, scene_obj)
        
        if intersect == None or recursion >= MAX_RECURSION_DEPTH:            
            return self.env_map.get_env_color(dir) if self.env_map else (self.clear_color[0] / 255, self.clear_color[1] / 255, self.clear_color[2] / 255)
                
        material = intersect.scene_obj.material
        
        final_color = [0, 0, 0]
        object_color = [material.diffuse[0], material.diffuse[1], material.diffuse[2]]
                            
        if material.mat_type == OPAQUE:
            for light in self.lights:
                diffuse_color = light.get_diffuse_color(intersect, self)
                spec_color = light.get_spec_color(intersect, self)
                shadow_intensity = light.get_shadow_intensity(intersect, self)

                light_color = mf.multiply_matrix_by_a_value(mf.add(diffuse_color, spec_color), (1 - shadow_intensity))
                final_color = mf.add(final_color, light_color)

        elif material.mat_type == REFLECTIVE:
            reflect = reflect_vector(intersect.normal, mf.multiply_matrix_by_a_value(dir, -1))
            reflect_color = self.cast_ray(intersect.point, reflect, intersect.scene_obj, recursion + 1)

            spec_color = [0,0,0]
            for light in self.lights:
                spec_color = mf.add(spec_color, light.get_spec_color(intersect, self))

            final_color = mf.add(reflect_color, spec_color)

        elif material.mat_type == TRANSPARENT:
            outside = mf.dot(dir, intersect.normal) < 0
            bias = mf.multiply_matrix_by_a_value(intersect.normal, 0.001)

            spec_color = [0, 0, 0]
            for light in self.lights:
                spec_color = mf.add(spec_color, light.get_spec_color(intersect, self))

            reflect = reflect_vector(intersect.normal, mf.multiply_matrix_by_a_value(dir, -1))            
            reflect_orig = mf.add(intersect.point, bias) if outside else mf.subtract_arrays(intersect.point, bias)            
            reflect_color = self.cast_ray(reflect_orig, reflect, None, recursion + 1)
            
            kr = fresnel(intersect.normal, dir, material.ior)
            
            refract_color = [0, 0, 0]
            if kr < 1:
                refract = refract_vector(intersect.normal, dir, material.ior)
                refract_origin = mf.subtract_arrays(intersect.point, bias) if outside else mf.add(intersect.point, bias)            
                refract_color = self.cast_ray(refract_origin, refract, None, recursion + 1)
                
            colors_res = mf.add(mf.multiply_matrix_by_a_value(reflect_color, kr), mf.multiply_matrix_by_a_value(refract_color, (1 - kr)))
            final_color = mf.add(colors_res, spec_color)

        final_color = mf.multiply_two_lists_or_arrays(final_color, object_color)

        if material.texture and intersect.texcoords:
            tex_color = material.texture.get_color(intersect.texcoords[0], intersect.texcoords[1])

            if tex_color is not None:            
                final_color = mf.multiply_two_lists_or_arrays(final_color, tex_color) # ! Probablemente habrá un error ahí

        r = min(1, final_color[0])
        g = min(1, final_color[1])
        b = min(1, final_color[2])
        
        return (r, g, b)
    
    def gl_render(self) -> None:
        # Proyeccion
        t = tan((self.fov * mf.pi() / 180) / 2) * self.near_plane
        r = t * self.vp_width / self.vp_height
            
        for y in range(self.vp_y, self.vp_y + self.vp_height + 1):
            for x in range(self.vp_x, self.vp_x + self.vp_width + 1):
                # Pasar de coordenadas de ventana a coordenadas NDC (-1 a 1)
                p_x = ((x + 0.5 - self.vp_x) / self.vp_width) * 2 - 1
                p_y = ((y + 0.5 - self.vp_y) / self.vp_height) * 2 - 1
                                                
                p_x *= r
                p_y *= t
                
                direction = V3(p_x, p_y, -self.near_plane)                
                direction = mf.divition([direction.x, direction.y, direction.z], mf.norm([direction.x, direction.y, direction.z]))
                
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
                    
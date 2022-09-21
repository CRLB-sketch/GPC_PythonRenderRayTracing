########################################################################################
"""
    Universidad del Valle de Guatemala
    Graficas por Computadora
    Python Render3D
"""
__author__ = "Cristian Laynez 201281"
__status__ = "Student of Computer Science"

# ! Texture : Clase donde se guardará la información de la textura a crear
# Referencias de Carlos Alonso proporcionado en clase
######################################################################################

import struct

from MathFake import MathFake as mf
from math import atan2 as arctan2
from math import acos as arccos

class Texture(object):
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            header_size = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(header_size)

            self.pixels = []

            for y in range(self.height):
                pixelRow = []

                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    pixelRow.append([r,g,b])

                self.pixels.append(pixelRow)

    def get_color(self, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return self.pixels[int(v * self.height)][int(u * self.width)]     
        return None
    
    def get_env_color(self, dir):
        dir = mf.divition(dir, mf.norm(dir))
        
        x = int((arctan2(dir[2], dir[0]) / (2 * mf.pi()) + 0.5) * self.width)
        y = int(arccos(-dir[1]) / mf.pi() * self.height)
        
        return self.pixels[y][x]

# Referencias de Carlos Alonso proporcionado en clase
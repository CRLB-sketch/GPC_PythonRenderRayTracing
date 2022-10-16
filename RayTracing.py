from GlRender import *

from Figures import *
from Lights import *

width = 512
height = 512

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec = 64, mat_type= REFLECTIVE)
glass = Material(diffuse= (0.9, 0.9, 0.9), spec=64, ior = 1.5, mat_type= TRANSPARENT)
marble = Material(spec = 64, texture = Texture("textures/marble.bmp"), mat_type= REFLECTIVE)

wall = Material(diffuse = (0.14, 0.58, 0.75), spec = 8)
baby_blue = Material(diffuse=(0, 0, 1), spec = 64, mat_type=OPAQUE)

rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/landscape.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( PointLight( point = (-1, -1, 0) ))

# Primer Triangulo
rtx.scene.append(Triangle(A = V3(-1.9, -1.5, -3.5), B = V3(0, -1.5, -3.5), C = V3(-0.95, 0, -3.5), material = baby_blue))

# Segundo Triangulo
rtx.scene.append(Triangle(A = V3(0, -1.5, -3.5), B = V3(1.9, -1.5, -3.5), C = V3(0.95, 0, -3.5), material = marble))

# Tercer Triangulo
rtx.scene.append(Triangle(A = V3(-0.95, 0, -3.5), B = V3(0.95, 0, -3.5), C = V3(0, 1.5, -3.5), material = mirror))

rtx.gl_render()

rtx.gl_finish("outputs/output_lab_3.bmp")
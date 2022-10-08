from GlRender import *

from test import *

from Figures import *
from Lights import *
from outputs.test import testing_func

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

# ! - Escenario Cuarto Chilero

rtx.env_map = Texture("textures/parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( PointLight( point = (-1, -1, 0) ))

# Triangulos
rtx.scene.append ( Triangle(A = V3(1, 0, 0), B = V3(1, -1, 0), C = V3(0, 0, -1), material = baby_blue))

rtx.gl_render()

rtx.gl_finish("outputs/output_lab_3.bmp")
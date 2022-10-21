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

rtx.env_map = Texture("textures/stars_landscape.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( PointLight( point = (-1, -1, 0) ))

# ! PREPARAR ESCENA PARA PROYECTO 2 ------------------------------------

rtx.scene.append( Plane(position = (0,-10,0), normal = (0,1,0), material = brick ))

rtx.scene.append( AABB(position = (0, 0.5, -12.5), size = (15, 6, 2), material = brick)) # Pared de fondo

rtx.scene.append( AABB(position = (0, -3, -11), size = (15, 0.3, 5), material = baby_blue))
rtx.scene.append( AABB(position = (0, -2.5, -10), size = (15, 0.3, 2), material = baby_blue))

rtx.scene.append( AABB(position = (5,0,-10), size = (2,6.5,6), material = brick)) # Pared derecho
rtx.scene.append( AABB(position = (-5,0,-10), size = (2,6.5,6), material = brick)) # Pared izquierdo

rtx.gl_render()

rtx.gl_finish("outputs/output_proyecto_2.bmp")
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

# ! INTENTO TORUS ------------------------------------------------------
# Prueba Torus
# rtx.scene.append( Torus([0, 0, 0], 0.5, 0.6, baby_blue))
# rtx.scene.append( Torus([0, 0, 0], 0.5, 0.4, baby_blue)) # NEL
# rtx.scene.append( Torus([0, 0, 0], 0.4, 0.5, baby_blue)) # Solo bordes
# rtx.scene.append( Torus([0, 0, 0], 0.4, 0.4, baby_blue))
# rtx.scene.append( Torus([0, 0, 0], 0.1, 0.2, baby_blue))

# ! PREPARAR ESCENA PARA PROYECTO 2 ------------------------------------

rtx.scene.append( Disk(position = (0,-2,-7), radius = 3, normal = (0,1,0), material = baby_blue ) )

# # ! TESTING:
# rtx.scene.append( Plane(position = (0,-10,0), normal = (0,1,0), material = brick ))
# rtx.scene.append( Plane(position = (0,10,0), normal = (0,-1,0), material = brick ))
# rtx.scene.append( Plane(position = (-10,0,0), normal = (1,0,0), material = stone ))
# rtx.scene.append( Plane(position = (10,0,0), normal = (-1,0,0), material = stone ))
# rtx.scene.append( Plane(position = (0,0,-40), normal = (0,0,1), material = stone ))

# rtx.scene.append( Disk(position = (0,-3,-7), radius = 2, normal = (0,1,0), material = mirror ))

# rtx.scene.append( AABB(position = (-2,1,-10), size = (2,2,2), material = glass))
# rtx.scene.append( AABB(position = (2,1,-10), size = (2,2,2), material = marble))

rtx.gl_render()

rtx.gl_finish("outputs/output_proyecto_2.bmp")
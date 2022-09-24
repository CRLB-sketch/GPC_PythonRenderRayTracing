from GlRender import *

from Figures import *
from Lights import *

width = 1024
height = 1024

# ! -----------------------------------------------------------------------------------------------
# ! - Mis propios materiales jaja!

# TODO: Materiales Opacos
earth = Material(texture = Texture('textures/earthDay.bmp'), mat_type=OPAQUE)
moon = Material(texture = Texture('textures/moon.bmp'), mat_type=OPAQUE)

# TODO: Materiales Reflectivos
marble = Material(diffuse= (0.8, 0.8, 0.8), texture = Texture('textures/marble.bmp'), spec = 32, mat_type = REFLECTIVE)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec = 64, mat_type= REFLECTIVE)

# TODO: Materiales Transparentes
water = Material(diffuse= (0.9, 0.9, 0.9), texture = Texture('textures/water_transparent.bmp'), spec=64, ior = 1.5, mat_type= TRANSPARENT)
diamond = Material(diffuse= (0.9, 0.9, 0.9), spec=64, ior = 2.417, mat_type= TRANSPARENT)

# ! -----------------------------------------------------------------------------------------------
# ! - Preparando RayTracer para iniciar renderizaje -----------------------------------------------
rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/landscape.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( DirectionalLight(direction= (-1, -1, -1), intensity= 0.8))

rtx.scene.append( Sphere(V3(-3.5, 2, -10), 1.5, earth))
rtx.scene.append( Sphere(V3(-3.5, -2, -10), 1.5, moon))

rtx.scene.append( Sphere(V3(0, 2, -10), 1.5, marble))
rtx.scene.append( Sphere(V3(0, -2, -10), 1.5, mirror))

rtx.scene.append( Sphere(V3(3.5, 2, -10), 1.5, water))
rtx.scene.append( Sphere(V3(3.5, -2, -10), 1.5, diamond))

rtx.gl_render()

rtx.gl_finish("outputs/output_rt2_.bmp")
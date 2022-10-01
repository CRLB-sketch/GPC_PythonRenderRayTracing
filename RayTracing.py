from GlRender import *

from Figures import *
from Lights import *

width = 256
height = 256

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec = 64, mat_type= REFLECTIVE)
glass = Material(diffuse= (0.9, 0.9, 0.9), spec=64, ior = 1.5, mat_type= TRANSPARENT)

wall = Material(diffuse = (0.14, 0.58, 0.75), spec = 8)
baby_blue = Material(diffuse=(0, 0, 1), spec = 64, mat_type=OPAQUE)

rtx = Raytracer(width, height)

# ! - Escenario Cuarto Chilero

# rtx.env_map = Texture("textures/parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( DirectionalLight(direction= (-1, -1, -1), intensity= 0.8))
rtx.lights.append( PointLight( point = (0, 0, 0) ))

# Paredes
rtx.scene.append( Plane(position=(0, -10, 0), normal=(0, 1, 0), material=wall))
rtx.scene.append( Plane(position=(0, 20, 0), normal=(0, 1, 0), material=brick))
rtx.scene.append( Plane(position=(-10, 0, 0), normal=(1, 0, 0), material=brick))
rtx.scene.append( Plane(position=(10, 0, 0), normal=(1, 0, 0), material=brick))
rtx.scene.append( Plane(position=(0, 0, -50), normal=(0, 0, 1), material=brick))

# Cuadros
rtx.scene.append( AABB(position=(2, -2, -10), size=(2, 2, 2), material= mirror))
rtx.scene.append( AABB(position=(-2, -2, -10), size=(2, 2, 2), material= baby_blue))

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( DirectionalLight(direction= (-1, -1, -1), intensity= 0.8))

rtx.gl_render()

rtx.gl_finish("outputs/output_rt3.bmp")
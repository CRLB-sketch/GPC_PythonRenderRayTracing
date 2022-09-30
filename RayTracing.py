from GlRender import *

from Figures import *
from Lights import *

width = 256
height = 256

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec = 64, mat_type= REFLECTIVE)
glass = Material(diffuse= (0.9, 0.9, 0.9), spec=64, ior = 1.5, mat_type= TRANSPARENT)

# marble = Material(spec = 64, texture = Texture('marble.bmp'), mat_Type= REFLECTIVE) # Para el escenario 2
rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/parkingLot.bmp")

# rtx.scene.append( Plane(position=(0, -10, 0), normal=(0, 1, 0), material=brick))

# ! - Escenario 1

# rtx.lights.append( AmbientLight(intensity= 0.1))
# rtx.lights.append( DirectionalLight(direction= (-1, -1, -1), intensity= 0.8))

# # rtx.scene.append( Plane(position=(0, -10, 0), normal = (0, 1, 0), brick))
# # rtx.scene.append( Plane(position=(0, -10, 0), normal=(0, 1, 0), material=brick))

# rtx.scene.append( AABB(position=(2, 2, -10), size=(2, 2, 2), material= brick))
# rtx.scene.append( AABB(position=(-2, 2, -10), size=(2, 2, 2), material= stone))

# rtx.scene.append( AABB(position=(2, -2, -10), size=(2, 2, 2), material= mirror))
# rtx.scene.append( AABB(position=(-2, -2, -10), size=(2, 2, 2), material= glass))

# ! - Escenario 2

rtx.scene.append( Disk(position=(0, 2, 0), normal = (0, 1,0 ), material = brick, radius = 3))

# rtx.scene.append( AABB(position = (2, 2, -10), size=(2, 2, 2), material=glass))

# Falla con lo siguiente: glass, mirror, 

rtx.gl_render()

rtx.gl_finish("outputs/output_example.bmp")
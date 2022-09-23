from GlRender import *

from Figures import *
from Lights import *

width = 1024
height = 1024

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec = 64, mat_type= REFLECTIVE)
glass = Material(diffuse= (0.9, 0.9, 0.9), spec=64, ior = 1.5, mat_type= TRANSPARENT)

rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( DirectionalLight(direction= (-1, -1, -1), intensity= 0.8))

rtx.scene.append( Sphere(V3(0, 0, -10), 3, glass))

rtx.gl_render()

rtx.gl_finish("outputs/example_transparent.bmp")
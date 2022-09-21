from GlRender import *

from Figures import *
from Lights import *

width = 1024
height = 1024

# Materiales para el muñeco de nieve
snow = Material(diffuse=(0.9, 0.9, 0.9))
buttons = Material(diffuse=(0.2, 0.2, 0.2))
mouth = Material(diffuse = (0.4, 0.4, 0.4))
carriot = Material(diffuse=(1, 0.5, 0))
eyes = Material()
eyeslids = Material(BLACK)

rtx = Raytracer(width, height)

brick = Material(diffuse= ())

# glass = Material(diffuse= (0.9, 0.9, 0.9), spec = 64, matType = TRANSPARENT)


rtx.gl_render()

rtx.gl_finish("outputs/output.bmp")
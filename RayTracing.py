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

rtx.lights.append( AmbientLight() )
rtx.lights.append( DirectionalLight(direction=(-1, -1, -1)) )

# !- Cuerpo del muñeco de nieve
rtx.scene.append( Sphere(V3(0,-2.5,-9), 2, snow)  ) # Abajo
rtx.scene.append( Sphere(V3(0,0,-9.5), 1.9, snow)  ) # En medio
rtx.scene.append( Sphere(V3(0,2.5,-9), 1.5, snow)  ) # Arriba

# !- Botones para el muñeco de nieve
rtx.scene.append( Sphere(V3(0,-2,-7), 0.5, buttons)  ) # Abajo
rtx.scene.append( Sphere(V3(0,-0.7,-7.5), 0.4, buttons)  ) # En medio
rtx.scene.append( Sphere(V3(0,0.7,-7.8), 0.3, buttons)  ) # Arriba

# !- Sonrisa Colgate :)
rtx.scene.append( Sphere(V3(-0.6, 1.7, -7.8), 0.2, mouth)  ) # Esfera 1
rtx.scene.append( Sphere(V3(-0.3, 1.3, -7.8), 0.2, mouth)  ) # Esfera 2
rtx.scene.append( Sphere(V3(0.3, 1.3, -7.8), 0.2, mouth)  ) # Esfera 3
rtx.scene.append( Sphere(V3(0.6, 1.7, -7.8), 0.2, mouth)  ) # Esfera 4

# !- Nariz de zanahoria
rtx.scene.append( Sphere(V3(0, 2.2, -7.8), 0.5, carriot)  )

# !- Ojos del muñeco de nieve
rtx.scene.append( Sphere(V3(-0.4, 2.8, -7.8), 0.3, eyes)  ) # Ojo Izquierdo
rtx.scene.append( Sphere(V3(0.4, 2.8, -7.8), 0.3, eyes)  ) # Ojo Derecho

# !- Parpados
rtx.scene.append( Sphere(V3(-0.4, 2.9, -7.6), 0.14, eyeslids)  ) # Parpado Izquierdo
rtx.scene.append( Sphere(V3(0.4, 2.9, -7.6), 0.14, eyeslids)  ) # Parpado Derecho


rtx.gl_render()

rtx.gl_finish("outputs/output.bmp")
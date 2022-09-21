from GlRender import *

from Figures import *
from Lights import *

width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3), spec = 16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, mat_type = REFLECTIVE)
blueMirror = Material(diffuse = (0.2, 0.2, 0.9), spec = 64, mat_type = REFLECTIVE)
yellowMirror = Material(diffuse = (0.9, 0.9, 0.2), spec = 64, mat_type = REFLECTIVE)

rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/parkingLot.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
#rtx.lights.append( PointLight(point = (0,0,0)))

rtx.scene.append( Sphere(V3(0,0,-10), 1, mirror)  )

rtx.scene.append( Sphere(V3(3,0,-10), 1, brick)  )
rtx.scene.append( Sphere(V3(0,3,-10), 1, stone)  )

rtx.scene.append( Sphere(V3(-3,0,-10),1, blueMirror)  )
rtx.scene.append( Sphere(V3(0,-3,-10), 1, yellowMirror)  )


rtx.gl_render()

rtx.gl_finish("outputs/example_sucess1.bmp")
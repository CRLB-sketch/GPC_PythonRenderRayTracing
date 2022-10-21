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
baby_blue = Material(diffuse = (0.14, 0.58, 0.75), spec = 64, mat_type=OPAQUE)

baby_blue_light = Material(diffuse=(0.67, 0.78, 0.85), spec=64)
wood = Material(diffuse=(0.58, 0.57, 0.50), spec=64)
green_soft = Material(diffuse=(0.43, 0.56, 0.60), spec=64)
floor_orange = Material(diffuse=(0.83, 0.62, 0.14), spec=64)
green = Material(diffuse=(0.6, 0.48, 0), spec=64)

rtx = Raytracer(width, height)

rtx.env_map = Texture("textures/stars_landscape.bmp")

rtx.lights.append( AmbientLight(intensity= 0.1))
rtx.lights.append( PointLight( point = (-1, -1, 0) ))

# ! PREPARAR ESCENA PARA PROYECTO 2 ------------------------------------

rtx.scene.append( Plane(position = (0,-10,0), normal = (0,1,0), material = floor_orange )) # Simular Suelo naranja
rtx.scene.append( Plane(position = (0,10,0), normal = (0,-1,0), material = glass )) # Simular techo de vidrio

rtx.scene.append( AABB(position = (0, 0.3, -15), size = (15, 6, 2), material = baby_blue_light)) # Pared de fondo

rtx.scene.append( AABB(position = (0, -3, -11), size = (12, 0.3, 5), material = wood)) # Primera grada madera
rtx.scene.append( AABB(position = (0, -2.7, -10), size = (12, 0.3, 2), material = wood)) # Segunda grada de madera

rtx.scene.append( AABB(position = (0, -2, -11), size = (6, 0.7, 3), material = green) ) # Representar cama chafa xd

rtx.scene.append( AABB(position = (5,0,-11), size = (2,6.5,9), material = baby_blue_light)) # Pared derecho
rtx.scene.append( AABB(position = (-5,0,-11), size = (2,6.5,9), material = baby_blue_light)) # Pared izquierdo

# -> Preparar puerta
rtx.scene.append( AABB(position = (4, -0.65, -10), size = (0.2, 5, 2), material = wood) )

# -> Preparar armario de madera
rtx.scene.append( AABB(position = (-4.05, 0, -14), size = (1, 2, 2), material = wood) ) # El Coso de madera
rtx.scene.append(Triangle(A = V3(-4.6, -1, -13.1), B = V3(-4.6, -2, -13.1), C = V3(-3.55, -1, -13.1), material = wood))

rtx.scene.append( AABB(position = (-4.05, 0, -14), size = (1, 2, 2), material = wood) ) # El Coso de madera
rtx.scene.append(Triangle(A = V3(-4.6, -1, -13.1), B = V3(-4.6, -2, -13.1), C = V3(-3.55, -1, -13.1), material = wood))

# -> Preparar espejo
rtx.scene.append( AABB(position = (-4.05, 0, -10), size = (0.2, 2, 2), material = mirror) ) # El vidrio

rtx.scene.append( AABB(position = (-4.01, -1.08, -10), size = (0.4, 0.15, 2.2), material = wood) ) # Barra abajo
rtx.scene.append( AABB(position = (-4.01, 1.08, -10), size = (0.4, 0.15, 2.2), material = wood) ) # barra arriba

rtx.scene.append( AABB(position = (-4.01, 0, -9), size = (0.4, 2, 0.2), material = wood) ) # barra izquierda
rtx.scene.append( AABB(position = (-4.01, 0, -11), size = (0.4, 2, 0.2), material = wood) ) # barra derecha

rtx.gl_render()

rtx.gl_finish("outputs/output_proyecto_2.bmp")
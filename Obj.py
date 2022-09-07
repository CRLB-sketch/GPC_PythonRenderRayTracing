########################################################################################
"""
    Universidad del Valle de Guatemala
    Graficas por Computadora
    Python Render3D
"""
__author__ = "Cristian Laynez 201281"
__status__ = "Student of Computer Science"

# ! Obj : Clase donde se leerá la información del Objeto 3D
# Referencias de Carlos Alonso proporcionado en clase
######################################################################################

class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []

        self.__prepare_lines()

    def __prepare_lines(self):
        for line in self.lines:
            try:
                prefix, value = line.split(' ', 1)
            except:
                continue

            if prefix == 'v': # Vertices
                self.vertices.append( list(map(float,value.split(' '))))
            elif prefix == 'vt':
                self.texcoords.append( list(map(float, value.split(' '))))
            elif prefix == 'vn':
                self.normals.append( list(map(float, value.split(' '))))
            elif prefix == 'f':
                self.faces.append([  list(map(int, vert.split('/'))) for vert in value.split(' ')] )

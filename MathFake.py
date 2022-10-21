########################################################################################
"""
    Universidad del Valle de Guatemala
    Graficas por Computadora
    Python Render3D
"""
__author__ = "Cristian Laynez 201281"
__status__ = "Student of Computer Science"

# ! Math Fake : Clase/Libreria donde estarán las funciones matemáticas y de AL
# TODO: La clase matemática más MotherF*cker que vas a conocer >:)
######################################################################################

from collections import namedtuple
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

from math import sqrt
from math import acos as arccos
from math import cos
from math import atan2 as arctan2

import decimal
decimal.getcontext().prec = 100

# * -------------------------------------------------------------------------------------
# * CLASE MOTHERF*UCKER de MathFaKe -----------------------------------------------------
class MathFake:
                  
    """ 
    Identity / Identidad:
        Al ingresar un tamaño en específico te crea una matriz identidad
    Params:
        size - int: Tamaño de matriz identidad a crear
    Returns:
        matrix: retorna la nueva matriz identidad
    """  
    @staticmethod
    def identity(size : int) -> list:
        return [[1 if x == y else 0 for y in range(0, size)] for x in range(0, size)]
    
    """
    Multiply Two Lists/Arrays:
        Al ingresar dos listas/arrays del mismo tamaño se multiplicarán
    Params:
        array1 - list: Array/Lista numero 1 a multiplicar
        array2 - list: Array/Lista numero 2 a multiplicar
    Returns:
        list/array: Retorna la nueva lista/array multiplicada
    """
    @staticmethod
    def multiply_two_lists_or_arrays(array1 : list, array2 : list):
        return [(array1[i] * array2[i]) for i in range(len(array1))]
    
    """ 
    Multiply Matrixs / Multiplicar Matrices:
        Puedes ingresar todas las matrices que se te de la 
        REGALADA gana (siempre y cuando sean del mismo tamaño todos)
        y te lo multiplicará todo :)
    Params:
        all_matrixs - lista: Un listado de todas las matrices a multiplicar
    Returns:
        matrix: retorna el resultado de la multiplicación
    """
    @staticmethod
    def multiply_matrixs(all_matrixs : list) -> list:
        if len(all_matrixs) <= 1: return None
        for m in all_matrixs:
            if len(m) != len(m[0]): return None            
        size = len(m)
        result = [[ 0 for y in range(0, size)] for x in range(0, size)]        
        for m in range(0, len(all_matrixs)):
            matrix = all_matrixs[m] if m == 0 else result
            next_matrix = all_matrixs[m+1]
            for x in range(0, len(matrix)):
                for y in range(0, len(matrix)):
                    res = 0
                    for _ in range(0, len(matrix)):
                        res += (matrix[x][_] * next_matrix[_][y])
                    result[x][y] = float(res)
            if (m + 2) == len(all_matrixs): break            
        return result
        
    """ 
    Multiply Matrix And V4 / Multiplicar Matriz y V4:
        Se verifica si la matriz es 4 x 4
    Params:
        matrix 4x4 - list 4x4: Matriz a operar
        vector4 - V4: Vector4 a operar
    Returns:
        list: retorna el listado con sus correspondiente resultado
    """  
    @staticmethod
    def multiply_matrix_and_v4(matrix_4_x_4 : list, vector4 : V4) -> list:
        if len(matrix_4_x_4) != 4 and len(matrix_4_x_4[0]) != 4:
            return None                
        v4 = [
            [vector4.x],
            [vector4.y],
            [vector4.z],
            [vector4.w],
        ]
                
        result = [0 for x in range(0, 4)]
        for x in range(0, len(matrix_4_x_4)):
            res = 0
            for y in range(0, len(matrix_4_x_4[x])):
                res += float((matrix_4_x_4[x][y] * v4[y][0]))
            result[x] = res
        
        return result
    
    """
    Multiplicar entre matriz 3 x 3 y matriz 3 x 1:
        Se llevará a cabo una multiplicacion entre estas matrices en especial :)
    Params:
        matrix_a : Matriz 3 x 3
        list_b : Matriz 3 x 1
    Returns:
        list : La matriz ya multiplicada
    """
    @staticmethod
    def multiply_m3x3_and_m3x1(matrix_a : list, list_b : list) -> list:
        return [(matrix_a[i][0] * list_b[0]) + (matrix_a[i][1] * list_b[1]) + (matrix_a[i][2] * list_b[2]) for i in range(len(matrix_a))]
    
    """
    Multiplicar una matriz por un valor:
        Se recibirá una lista para multiplicar dicho valor
    Params:
        matrix_or_list : Realmente es una lista jaja
        the_value : Valor a multiplicar con la matriz
    Returns:
        list : Resultado de la multiplicación correspondiente
    """
    @staticmethod
    def multiply_matrix_by_a_value(matrix_or_list : list, the_value : float) -> list:
        return [(i * the_value) for i in matrix_or_list]
    
    """
    Add / Sumar:
        Sumar dos listas/arreglos del mismo tamaño
    Params:
        m_list1 & m_list2 : Recibir una lista o array con números
    Returns:
        list: Una lista con el resultado de la suma
    """
    @staticmethod
    def add(m_list1 : list, m_list2 : list) -> list:
        return [(m_list1[i] + m_list2[i]) for i in range(len(m_list1))]

    """
    Valores inversos para un array o lista:
        Los valores de la lista serán opuestos
    Params:
        array or list: Recibir una lista o array con números
    Returns:
        list: La lista con los números opuestos
    """
    @staticmethod
    def inverse_values_of_array_or_list(a_or_l) -> list:        
        return [(-i) for i in a_or_l]

    """
    Dot / Producto Punto:
        Llevar a cabo producto punto de dos listas
    Params:
        a1 & a2: Las listas que se van a operar
    Returns:
        float: Resultado de producto punto
    """
    @staticmethod
    def dot(a1 : list, a2 : list) -> float:
        if len(a1) != len(a2): return None        
        result = 0
        for i in range(0, len(a1)):            
            result += a1[i] * a2[i]                                
        return result
    
    """
    Cross / Producto Cruz:
        Llevar a cabo producto cruz con listas de 3 numeros
    Params:
        a & b: Las listas a operar
    Return:
        list: Lista con el resultado del producto cruz
    """
    @staticmethod
    def cross(a : list, b : list) -> list:
        if len(a) != 3 and len(b) != 3: return None
        i = ((a[1] * b[2]) - (a[2] * b[1]))
        j = ((a[0] * b[2]) - (a[2] * b[0]))
        k = ((a[0] * b[1]) - (a[1] * b[0]))
        return [i, -j, k]
            
    """
    Subtract V3 / Resta de Vectores V3:
        Se restarán dos arrays
    Params:
        a & b: Los arrays a operar
    Return:
        list: Resultado de la resta
    """    
    @staticmethod
    def subtract_arrays(a : list, b : list) -> list:        
        return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
    
    """
    Subtract V3 / Resta de Vectores V3:
        Se restarán dos vectores 3
    Params:
        a & b: Los vectores 3 a operar
    Return:
        list: Resultado de la resta
    """
    @staticmethod
    def subtract_V3(a : V3, b : V3) -> list:        
        return [a.x - b.x, a.y - b.y, a.z - b.z]
    
    """
    Norm / Normalizar:
        Se normalizará una lista dada (puede ser de cualquier tamaño)
    Params:
        data: La lista a normalizar
    Return:
        float: Resultado de la lista normalizada
    """
    @staticmethod
    def norm(data : list) -> float:
        result = 0
        for i in data:
            result += i**2            
        return pow(result, 0.5)
    
    """
    Division / Divition:
        Dividir lista entre el resultado de la normalización
    Params:
        a : Lista a dividir
        norm : El valor normalizado que se utilizará para dividir
    Return:
        list: La lista con todos los valores divididos
    """
    @staticmethod
    def divition(a : list, norm : float) -> list:
        return [(i / norm) for i in a]
    
    """
    Inversion:
        Obtener el inverso de una matriz por medio del método de gauss jordan 
    Params:
        matrix : La matriz a operar
    Return:
        list : La matriz ya con su resultado
    """
    @staticmethod
    def linalg_inversion(matrix : list) -> list:
        # Verificar que la matriz sea cuadrada
        size = len(matrix)
        if size != len(matrix[0]):
            return None
        
        # Se juntará la matriz con una matriz identidad conforme al tamaño solicitado
        m_identity = [[1 if x == y else 0 for y in range(0, size)] for x in range(0, size)]
        for i in range(size):
            matrix[i].extend(m_identity[i])
            
        # Algoritmo eliminación por medio del método de gauss jordan 
        for i in range(size):
            checking_matrix = matrix[i][i]
            if checking_matrix == 0:
                return "ERROR: LA MATRIZ NO ES INVERTIBLE"
                        
            for j in range(i, 2 * size):
                matrix[i][j] /= checking_matrix
            for z in range(size):
                if z == i or matrix[z][i] == 0: continue
                factor = matrix[z][i]
                for j in range(i, 2*size):
                    matrix[z][j] -= factor * matrix[i][j]
                
        return [[matrix[i][j] for j in range(size, len(matrix[0]))] for i in range(size)]
            
    """
    Pi:
        Número de Pi más aproximado
    Return:
        float : Número Pi
    """
    @staticmethod
    def pi() -> float: return 3.14159265358979323
    
    """
    Epsilon: Número de Epsilon más aproximado
    
    Return:
        float : Valor Epsilon
    """    
    @staticmethod
    def epsilon() -> float: return 0.001
    
    """
    Epsilon: Número de Epsilon más aproximado
    
    Return:
        float : Valor Epsilon
    """    
    @staticmethod
    def k_epsilon() -> float: return 0.0001
    
    """
    Sqrt: Raíz al cuadrado
    
    Return:
        float : Valor raíz al cuadrado del número ingresado
    """
    def mf_sqrt(number : float) -> float: 
        # number = round(number, 20)
        # return number ** 2
        return sqrt(number)
    
    """
    cbrt:
        Raíz Cubica
    Return:
        float : Valor raíz cubica del número ingresado
    """
    def cbrt(number : float) -> float: 
        if number < 0:
            number = abs(number)
            return number ** (1 / 3) * (-1)
        return number ** (1 / 3)
    
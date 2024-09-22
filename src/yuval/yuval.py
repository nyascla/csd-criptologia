"""
algoritmo de yuval

objetivo: conseguir que una victima firme un documento sin darse cuenta

dos mensajes de partida,
- uno bueno: uno que la victuma firme con gusto
- uno malo: uno que es veneficioso para el atacante

para este ejemplo trabajaremos con una funcion resumen de 40bits
pasos:
- tenemos que generar 2^m/2 modificaciones del mensaje bueno
- guardaremos el hash de cada mensaje modificado

requisito, mi nombre tiene que estar en el mensaje legitimo y el del profesor en el ilegitimo
"""

import hashlib
import itertools
from typing import List

with open('text_blanco.txt', 'r') as archivo:
    BLANCO = archivo.readlines()

with open('text_negro.txt', 'r') as archivo:
    NEGRO = archivo.readlines()


def hash_string(s):
    """Genera un hash de 40 bits a partir de una cadena."""
    # convierte la cadena en bytes, algoritmos operan en formato binario.
    # devuelve el hash en formato hexadecimal.
    # carácter hexadecimal 4 bits x 10 = 40 bits.
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def combined_text(code: List[int]):
    r = BLANCO.copy()
    for line, c in enumerate(code):
        if c > 0:
            r[line] = NEGRO[line]

    return "".join(r)


if "__main__" == __name__:

    combinations = itertools.product([0, 1], repeat=20)

    dic = {}
    try:
        for combination in combinations:
            print(combination)
            text = combined_text(combination)
            dic[hash_string(text)] = combination

    except:
        print("colision")

'''
DUDAS
hash de un fichero vs el hash de una string
- Hash de un archivo: Cuando calculas el hash de un archivo, estás procesando la representación binaria del archivo tal como está en el sistema de archivos. Esto incluye no solo el contenido textual, sino también cualquier metadato y formato que pueda estar presente.
- Hash de una cadena: Al calcular el hash de una cadena en Python, simplemente estás hasheando la secuencia de caracteres en esa cadena, sin incluir ningún formato adicional.
'''

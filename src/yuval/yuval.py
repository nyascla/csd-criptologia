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

with open('blanco.txt', 'r') as archivo:
    BLANCO = archivo.readlines()

with open('blanco1.txt', 'r') as archivo:
    BLANCO1 = archivo.readlines()

with open('negro.txt', 'r') as archivo:
    NEGRO = archivo.readlines()

with open('negro1.txt', 'r') as archivo:
    NEGRO1 = archivo.readlines()


def hash_string(s):
    """Genera un hash de 40 bits a partir de una cadena."""
    # convierte la cadena en bytes, algoritmos operan en formato binario.
    # devuelve el hash en formato hexadecimal.
    # carácter hexadecimal 4 bits x 10 = 40 bits.
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def blanco_combined_text(code: List[int]):
    r = BLANCO.copy()
    for line, c in enumerate(code):
        if c > 0:
            r[line] = BLANCO1[line]

    return "".join(r)


def negro_combined_text(code: List[int]):
    r = NEGRO.copy()
    for line, c in enumerate(code):
        if c > 0:
            r[line] = NEGRO1[line]

    return "".join(r)


if "__main__" == __name__:
    combinations = list(itertools.product([0, 1], repeat=20))

    dic_blanco = {}
    print(f"crea dic_blanco")
    for combination in combinations:
        text = blanco_combined_text(combination)
        key = hash_string(text)
        dic_blanco[key] = combination
    print(f"dic_blanco keys:{len(dic_blanco.keys())}")

    cont = 0
    colision = False
    while not colision:
        print(f"round: {cont}")
        for combination in combinations:
            text = negro_combined_text(combination)
            key = hash_string(text)
            if key in dic_blanco:
                print(f"COLISION: {combination}:{key}")
                colision = True
                break

        cont += 1

'''
DUDAS
hash de un fichero vs el hash de una string
- Hash de un archivo: Cuando calculas el hash de un archivo, estás procesando la representación binaria del archivo tal como está en el sistema de archivos. Esto incluye no solo el contenido textual, sino también cualquier metadato y formato que pueda estar presente.
- Hash de una cadena: Al calcular el hash de una cadena en Python, simplemente estás hasheando la secuencia de caracteres en esa cadena, sin incluir ningún formato adicional.
'''

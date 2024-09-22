import hashlib
import itertools

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

with open('text_blanco.txt', 'r') as archivo:
    text_blanco = archivo.readlines()

with open('text_negro.txt', 'r') as archivo:
    text_negro = archivo.readlines()

x = hashlib.sha256("".join(text_negro).encode("utf-8"))
print(x.hexdigest())
"""
combinaciones = itertools.product(text_blanco, text_negro)

diccionario_combinaciones = {f"combinacion_{i+1}": bin(i) for i, comb in enumerate(combinaciones)}

# Mostrar el resultado (opcional)
for clave, valor in diccionario_combinaciones.items():
    print(f"{clave}: {valor}")
    
"""


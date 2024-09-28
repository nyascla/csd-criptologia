"""
El propósito principal es revertir un hash a su valor original
(por ejemplo, una contraseña).

entrada de 40 bits
"""


if "__main__" == __name__:
    pass


"""
Require: Una función resumen h y una función recodificante r
Require: t longitud de la secuencia
Require: n número de entradas
Ensure: Una tabla rainbow para la función h.
tabla = tabla vacia
while La tabla no contenga n entradas do
    Escoger Pi un password al azar.
    P = Pi
    for j = 1 to t − 1 do
        P = r(h(P))
    end for
    Almacenar ⟨P1 , h(P)⟩ en la tabla
end while
"""
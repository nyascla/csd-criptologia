import hashlib
import os
from datetime import datetime

from logs.logger import get_logger

DIR = "logs/arcoiris"
os.makedirs(DIR, exist_ok=True)
FILE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
LOGPATH = os.path.join(DIR, FILE)

logger = get_logger(os.path.basename(__file__), LOGPATH)


def hash_string(s):
    """Genera un hash de 40 bits a partir de una cadena."""
    # convierte la cadena en bytes, algoritmos operan en formato binario.
    # devuelve el hash en formato hexadecimal.
    # carácter hexadecimal 4 bits x 10 = 40 bits.
    return hashlib.sha256(s.encode()).hexdigest()[:2]


palabras = ["Mesa", "Silla", "Computadora", "Ventana", "Libro", "Casa", "Perro", "Gato", "Árbol", "Cielo", "Sol",
            "Luna", "Estrella", "Mar", "Río", "Montaña", "Playa", "Jardín", "Flor", "Fruta", "Comida", "Agua", "Viento",
            "Nube", "Lluvia", "Fuego", "Tierra", "Camino", "Ciudad", "Pueblo", "Vehículo", "Tren", "Avión", "Bicicleta",
            "Reloj", "Teléfono", "Música", "Película", "Juego", "Arte", "Pintura", "Fotografía", "Palabra", "Historia",
            "Ciencia", "Matemáticas", "Geografía", "Tecnología", "Salud", "Sueño"]


def do(o):
    logger.info(f"objetivo: {o}")
    table = []
    for palabra in palabras:
        logger.info(f"fila: {palabra}")
        dic = dict()
        table.append(dic)

        p = palabra
        h = hash_string(p)
        for _ in range(10000000):
            dic[p] = h
            p = h
            h = hash_string(p)

            if h == o:
                logger.info(f"coincidencia:"
                            f"\n\n"
                            f"hash {o}: {hash_string(p)}"
                            f"palabra {o}: {hash_string(p)}")
                return

    for x in table:
        logger.info(f"{x}")


if "__main__" == __name__:
    OBJETIVO = "mama"
    HASH_OBJETIVO = hash_string(OBJETIVO)

    do(HASH_OBJETIVO)

"""
DUDAS:
porque una matriz y no un diccioanrio?
para que la funcion recodificante si el hash obtenido ya es una secuencia aleatoria
"""

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

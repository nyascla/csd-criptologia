import hashlib
import json
import os
import random
import time
from datetime import datetime

from arcoiris_config import CHARACTER_SPACE, PASSWORD_SIZE, HASH_SIZE, TABLE_SIZE, CHAIN_SIZE, NAME, PATH
from logs.logger import get_logger



def init_logger():
    dir = "logs/arcoiris"
    os.makedirs(dir, exist_ok=True)
    file = f"CREATE_{NAME}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"
    logfile = os.path.join(dir, file)

    return get_logger(os.path.basename(__file__), logfile)

def hash_string(s, size):
    """Genera un hash de 40 bits a partir de una cadena."""
    # convierte la cadena en bytes, algoritmos operan en formato binario.
    # devuelve el hash en formato hexadecimal.
    # carácter hexadecimal 4 bits x 10 = 40 bits.
    return hashlib.sha256(s.encode()).hexdigest()[:size]


def LEGACY_reduce_hex_to_n_digits(hex_str, n):
    """ probablemente no distribuirá los valores de forma uniforme """
    # Convertir la cadena hexadecimal a un número decimal
    decimal_value = int(hex_str, 16)

    # Obtener el valor máximo posible según la longitud de la cadena hexadecimal
    max_hex_value = int("F" * len(hex_str), 16)  # Por ejemplo, "FFF" para 3 caracteres, "FFFF" para 4, etc.

    # Escalar el valor decimal al rango de 0-999999 (o el valor máximo según el tamaño deseado)
    max_resultado_value = 10 ** n - 1  # El valor máximo según el tamaño del resultado
    scaled_value = int(decimal_value * (max_resultado_value / max_hex_value))

    # Formatear el número como una cadena con ceros a la izquierda según el tamaño deseado
    return f"{scaled_value:0{n}d}"


def LEGACYreduce_hex_to_n_digits(hex_str, n):
    """ probablemente no distribuirá los valores de forma uniforme """
    decimal_value = int(hex_str, 16)
    value = str(decimal_value)[-n:].zfill(n)  # ultimos n valores
    return value


def reduce_hex_to_n_digits(hex_str, n):
    """ mapeo modular genera una distribución más uniforme """
    # Convertir la cadena hexadecimal a un número decimal
    decimal_value = int(hex_str, 16)
    # Obtener el valor máximo posible para la longitud deseada
    max_resultado_value = 10 ** n - 1
    # Hacer un mapeo modular para obtener una distribución uniforme
    scaled_value = decimal_value % (max_resultado_value + 1)
    # Formatear el número como una cadena con ceros a la izquierda
    return f"{scaled_value:0{n}d}"


def generar_cadena():
    cadena = ''.join(random.choice(CHARACTER_SPACE) for _ in range(PASSWORD_SIZE))
    return cadena


def build_dataset():
    dataset = set()
    while len(dataset) < TABLE_SIZE:
        dataset.add(generar_cadena())

    return dataset


def build_table(dataset):
    start_time = time.perf_counter()
    password_unicas = set()

    l = init_logger()
    table = dict()

    for starting_point in dataset:
        end_point = build_chain(starting_point, l, password_unicas)
        if end_point in table:
            table[end_point].append(starting_point)
        else:
            table[end_point] = [starting_point]

    with open(PATH, "w") as archivo:
        json.dump(table, archivo)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    l.info(f"##### ##### ##### #####")
    l.info(f"password_unicas: {len(password_unicas)}")
    l.info(f"segundos:{elapsed_time} crear:{NAME}")


def build_chain(password, l, password_unicas):
    # s = ""
    for _ in range(CHAIN_SIZE):
        password_unicas.add(password)

        hash_password = hash_string(password, HASH_SIZE)
        next_password = reduce_hex_to_n_digits(hash_password, PASSWORD_SIZE)
        # s += f"{password} -H-> {hash_password} -R-> {next_password} | "

        password = next_password

    # l.info(s)

    return password


if "__main__" == __name__:
    x = "F" * HASH_SIZE
    d = int(x, 16)
    if len(str(d)) <= PASSWORD_SIZE:
        print("hash demasiado pequenyo, no abarca el espacio de claves")
        print(x, d, len(str(d)))
        exit()

    starting_points = build_dataset()
    build_table(starting_points)

    # for x in starting_points:
    #     h = hash_string(x, HASH_SIZE)
    #     r = reduce_hex_to_n_digits(h, PASSWORD_SIZE)
    #     print(f"{x} -H-> {h} -R-> {r} | ")

    # starting_points = build_dataset()
    # p = "000"
    # for _ in range(1000):
    #
    #     h = hash_string(p, HASH_SIZE)
    #     r = LEGACY_reduce_hex_to_n_digits(h, PASSWORD_SIZE)
    #     p = r
    #     print(r)


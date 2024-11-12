import hashlib
import json
import os
import random
import time
from datetime import datetime

from arcoiris_config import CHARACTER_SPACE, PASSWORD_SIZE, HASH_SIZE, TABLE_SIZE, CHAIN_SIZE, NAME, PATH
from logs.logger import get_logger
from arcoiris_reduces import reduccion

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
    s = ""
    for _ in range(CHAIN_SIZE):
        password_unicas.add(password)

        hash_password = hash_string(password, HASH_SIZE)
        funcion_reduccion = next(reduccion)
        next_password = funcion_reduccion(hash_password, PASSWORD_SIZE)
        s += f"{password} -H-> {hash_password} -R-{funcion_reduccion.__name__}-> {next_password} | "

        password = next_password

    l.info(s)

    return password


if "__main__" == __name__:
    x = "F" * HASH_SIZE
    d = int(x, 16)
    if len(str(d)) <= PASSWORD_SIZE:
        print("hash demasiado pequenyo, no abarca el espacio de claves")
        print(x, d, len(str(d)))
        exit()
    s = "354263"


    # starting_points = build_dataset()
    # build_table(starting_points)

    # for x in starting_points:
    #     h = hash_string(x, HASH_SIZE)
    #     r = reduce_hex_to_n_digits(h, PASSWORD_SIZE)
    #     print(f"{x} -H-> {h} -R-> {r} | ")

    starting_points = build_dataset()
    p = "309"
    hh = set()
    for _ in range(1000):
        h = hash_string(p, HASH_SIZE)
        funcion_reduccion = next(reduccion)
        r = funcion_reduccion(h, PASSWORD_SIZE)
        p = r
        hh.add(p)

    print(len(hh))

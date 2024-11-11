import json
import os
import time
from datetime import datetime
from math import floor

from arcoiris_config import PASSWORD_SIZE, HASH_SIZE, CHAIN_SIZE, PATH, NAME
from arcoiris_table import build_table, build_dataset, hash_string, generar_cadena
from logs.logger import get_logger
from arcoiris_reduces import generador_funciones_reduccion_inv, generador_funciones_reduccion, R

DIR = "logs/arcoiris"
os.makedirs(DIR, exist_ok=True)
FILE = f"CRACK_{NAME}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"
LOGPATH = os.path.join(DIR, FILE)

logger = get_logger(os.path.basename(__file__), LOGPATH)


def check_rainbow_table(table, target_hash):
    # Conjunto para almacenar posibles contraseñas únicas encontradas
    unique_passwords = set()

    step = 1

    while step <= CHAIN_SIZE:
        # Construir la lista de funciones de reducción aplicables
        reduction_functions = get_reduction_functions(step)

        logger.info(f"Step {step}: Using {len(reduction_functions)} reduction functions")

        current_hash = target_hash

        for func_index, reduction_func in enumerate(reduction_functions):
            # Generar una posible contraseña final usando la función de reducción
            potential_password = reduction_func(current_hash, PASSWORD_SIZE)

            logger.info(
                f"  Step {func_index}: Using {reduction_func.__name__} on hash {current_hash} -> Potential password: {potential_password}"
            )

            # Verificar si la contraseña posible está en la tabla y no ha sido probada
            if potential_password in table and potential_password not in unique_passwords:
                for initial_password in table[potential_password]:
                    cracked_password = check_chain(initial_password, target_hash)
                    if cracked_password:
                        return cracked_password

            # Agregar la contraseña generada a la lista de contraseñas únicas
            unique_passwords.add(potential_password)
            current_hash = hash_string(potential_password, HASH_SIZE)

        step += 1


def get_reduction_functions(step):
    """Devuelve la secuencia de funciones de reducción para un paso dado."""
    full_cycles = step // len(R)
    partial_cycle = step % len(R)

    # Construir la lista de funciones en el orden adecuado
    reduction_functions = R[-partial_cycle:] if partial_cycle > 0 else []
    reduction_functions += R * full_cycles

    return reduction_functions

# 16787 -H-> 2ed8e705dc -R-reduce_hex_to_n_digits-> 14588 | 14588 -H-> 9470307c22 -R-reduce_hex_with_multiplication-> 56518 | 56518 -H-> a7a285bea4 -R-reduce_hex_with_bit_manipulation-> 04048 | 04048 -H-> f79571532f -R-reduce_hex_rotate-> 18489 | 18489 -H-> 5d52bce12b -R-reduce_hex_with_string_manipulation-> 59541 | 59541 -H-> eadf8efacc -R-reduce_hex_sqrt-> 04376 | 04376 -H-> 7dacc04ac1 -R-reduce_hex_sin-> 16697 | 16697 -H-> 654c495ab1 -R-reduce_hex_power_mod-> 32527 | 32527 -H-> 279e8662a8 -R-reduce_hex_to_decimal-> 74865 | 74865 -H-> 498c9f9cfe -R-reduce_hex_to_decimal_v2-> 79005 |


def check_chain(starting_point, target_hash):
    reduccion_iterate_chain = generador_funciones_reduccion()

    password = starting_point
    for _ in range(CHAIN_SIZE):
        hash_password = hash_string(password, HASH_SIZE)

        if hash_password == target_hash:
            return password

        funcion_iterate_chain = next(reduccion_iterate_chain)
        next_password = funcion_iterate_chain(hash_password, PASSWORD_SIZE)
        password = next_password

    return


if "__main__" == __name__:
    x = "F" * HASH_SIZE
    d = int(x, 16)
    if len(str(d)) <= PASSWORD_SIZE:
        print("hash demasiado pequenyo, no abarca el espacio de claves")
        print(x, d, len(str(d)))
        exit()

    if not os.path.exists(PATH):
        logger.info(f"CREANDO TABLE: {PATH}")
        starting_points = build_dataset()
        build_table(starting_points)

    with open(PATH, "r") as archivo:
        rainbow_table = json.load(archivo)

    p = "838"
    target = hash_string(p, HASH_SIZE)

    encontrado = 0
    e = []
    noencontrado = 0
    noe = []
    startt_time = time.perf_counter()

    for _ in range(100):
        p = generar_cadena()
        target = hash_string(p, HASH_SIZE)

        start_time = time.perf_counter()
        logger.info(f"{p}")
        result = check_rainbow_table(rainbow_table, target)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"segundos: {elapsed_time} creackear: {NAME}")
        logger.info(f"hash objetivo: {target} password encontrado: {result}")

        if result:
            e.append(elapsed_time)
            logger.info(f":)")
            logger.info(f"Prueba con: {result}")
            logger.info(f"password secreta: {p}")
            encontrado += 1

        else:
            noe.append(elapsed_time)
            logger.info(f":'(")
            logger.info(f"password secreta: {p}")
            noencontrado += 1

    logger.info(f"### DATOS TOTALES {NAME}###")

    endd_time = time.perf_counter()
    elapsed_time = round(endd_time - startt_time, 10)
    logger.info(f"segundos totales: {elapsed_time}")

    logger.info(f"encontrado: {encontrado}")
    logger.info(f"no encontrado: {noencontrado}")

    logger.info(f"### TIEMPO COLISIONES ###")
    media = 0
    if len(e) > 0:
        media = sum(e) / len(e)
    logger.info(f"tiempo medio colision exitosa: {media}")

    media = 0
    if len(noe) > 0:
        media = sum(noe) / len(noe)
    logger.info(f"tiempo medio iteracion sin colision: {media}")

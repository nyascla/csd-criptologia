import json
import os
import time
from datetime import datetime

from arcoiris_config import PASSWORD_SIZE, HASH_SIZE, CHAIN_SIZE, PATH, NAME
from arcoiris_table import build_table, build_dataset, reduce_hex_to_n_digits, hash_string, generar_cadena
from logs.logger import get_logger

DIR = "logs/arcoiris"
os.makedirs(DIR, exist_ok=True)
FILE = f"CRACK_{NAME}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"
LOGPATH = os.path.join(DIR, FILE)

logger = get_logger(os.path.basename(__file__), LOGPATH)


def check_rainbow_table(table, target_hash):
    logger.info(f"### check_rainbow_table | target: {target_hash} ###")
    possible_end_password = reduce_hex_to_n_digits(target_hash, PASSWORD_SIZE)

    password_unicas = set()
    coincide_end_point = set()

    for xxx in range(CHAIN_SIZE):

        # logger.info(f"possible_end_password: {possible_end_password}")

        if possible_end_password in table and possible_end_password not in password_unicas:
            # logger.info(f"starting_points: {table[possible_end_password]}")
            for starting_point in table[possible_end_password]:
                cracked_password = check_chain(starting_point, target_hash)

                if cracked_password:
                    logger.info(f"##### ##### ##### #####")
                    logger.info(f"password_unicas: {len(password_unicas)}")

                    return cracked_password

        hash_password = hash_string(possible_end_password, HASH_SIZE)
        password_unicas.add(possible_end_password)
        possible_end_password = reduce_hex_to_n_digits(hash_password, PASSWORD_SIZE)

    logger.info(f"##### ##### ##### #####")
    logger.info(f"password_unicas: {len(password_unicas)}")


def check_chain(starting_point, target_hash):
    # logger.info(f"### check_chain | starting_point: {starting_point} target_hash: {target_hash} ###")

    password = starting_point
    for yyy in range(CHAIN_SIZE):
        hash_password = hash_string(password, HASH_SIZE)

        if hash_password == target_hash:
            logger.info(f"starting_point {starting_point} target: {target_hash} password: {password}")
            return password

        next_password = reduce_hex_to_n_digits(hash_password, PASSWORD_SIZE)

        password = next_password

    # logger.info(f"target NO encontrado")
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

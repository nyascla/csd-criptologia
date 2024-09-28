import logging



def get_logger(name, path, level=logging.DEBUG):
    logger = logging.getLogger(name)
    # Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Añadir los manejadores al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

if __name__ == '__main__':
    pass
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
import os
from datetime import datetime
from enum import Enum
from typing import Tuple

from logs.logger import get_logger

DIR = "logs/yuval"
os.makedirs(DIR, exist_ok=True)
FILE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
LOGPATH = os.path.join(DIR, FILE)

logger = get_logger(os.path.basename(__file__), LOGPATH)


class T(Enum):
    BLANCO = "blanco"
    NEGRO = "negro"
    TEST = "test"


def combine_texts(code: Tuple[int, ...], a, b):
    r = a.copy()
    for line, c in enumerate(code):
        if c > 0:
            r[line] = b[line]

    return "".join(r)


def hash_string(s):
    """Genera un hash de 40 bits a partir de una cadena."""
    # convierte la cadena en bytes, algoritmos operan en formato binario.
    # devuelve el hash en formato hexadecimal.
    # carácter hexadecimal 4 bits x 10 = 40 bits.
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def get_all_texts(t):
    """
    devuelve una lista con todos los textos
    la posicion 0 siempre estara el original
    """
    original = f"yuval/{t}/{t}.txt"
    variations_base = f"yuval/{t}/variations"

    r = []
    with open(original, 'r') as archivo:
        r.append(archivo.readlines())

    for file in os.listdir(variations_base):
        path = os.path.join(variations_base, file)
        with open(path, 'r') as archivo:
            r.append(archivo.readlines())

    return r


def do():
    combinations = list(itertools.product([0, 1], repeat=20))

    dic_blanco = {}
    texts_blanco = get_all_texts(T.BLANCO.value)
    for combination in combinations:
        text = combine_texts(combination, texts_blanco[0], texts_blanco[1])
        key = hash_string(text)
        dic_blanco[key] = combination
    logger.info(f"keys para el dic blanco: {len(dic_blanco)}")

    cont = 0
    texts_negro = get_all_texts(T.TEST.value)
    for text_to_combine in texts_negro[1:]:
        logger.info(f"randa: {cont}")
        d = 0
        for combination in combinations:
            text = combine_texts(combination, texts_negro[0], text_to_combine)
            key = hash_string(text)
            if key in dic_blanco:
                logger.info(f"colision key: {key} "
                            f"\n\n"
                            f"{combine_texts(dic_blanco[key], texts_blanco[0], texts_blanco[1])} "
                            f"\n\n"
                            f"{text}")

                return
        d += 1
        logger.info(f"randa: {cont} keys comparados: {d}")



        cont += 1


# f35efea57ee388945abec4d6a0480ec03cc20239e6bab54d3135c6e1a81af9da
# f35efea57e97355514972c5be2a6fdb19643fab7297a63d6d1ab4eb1a5e637c2



'''
DUDAS
hash de un fichero vs el hash de una string
- Hash de un archivo: Cuando calculas el hash de un archivo, estás procesando la representación binaria del archivo tal como está en el sistema de archivos. Esto incluye no solo el contenido textual, sino también cualquier metadato y formato que pueda estar presente.
- Hash de una cadena: Al calcular el hash de una cadena en Python, simplemente estás hasheando la secuencia de caracteres en esa cadena, sin incluir ningún formato adicional.
'''

"""En una pequeña aldea, vivía un anciano que conocía todos los secretos de las estrellas.
Cada noche, se sentaba bajo el cielo y contemplaba el universo, revelando sus misterios a quienes estaban dispuestos a escuchar.
Decía que cada estrella tenía una historia, y que cada constelación formaba un gran relato que abarcaba la historia de la humanidad.
Los habitantes del lugar solían acercarse para oír sus historias, y todos quedaban cautivados.
Las historias no solo hablaban de héroes y leyendas, sino también de eventos cósmicos y fenómenos naturales.
Para muchos, el sabio era un vínculo entre el pasado y el presente, entre lo terrenal y lo celestial.
Un día, un joven aventurero llegó a la aldea, ansioso por aprender sobre los secretos del cosmos.
El anciano le enseñó cómo las estrellas podían orientar a los viajeros y cómo los planetas influían en la vida diaria.
Juntos, pasaron muchas noches observando el cielo y descifrando los mensajes que las estrellas enviaban.
Con el tiempo, el joven se convirtió en un conocido astrónomo, llevando consigo las lecciones del anciano a rincones lejanos.
Aunque nunca olvidó su origen, sabía que había algo mágico en aquellos cielos del pueblo, donde los secretos del cosmos esperaban ser descubiertos.
El joven, ahora un experto en astronomía, regresaba a menudo a la aldea para compartir sus descubrimientos con el anciano.
Sus visitas se convirtieron en momentos de reflexión y aprendizaje, y el vínculo entre ellos se fortaleció con el tiempo.
Los aldeanos apreciaban cada visita, pues no solo aprendían sobre el cosmos, sino también sobre la conexión entre el ser humano y el universo.
La llegada del joven astrónomo trajo nueva vida al pueblo, llenándolo de curiosidad renovada y un sentido de asombro.
Las noches bajo las estrellas se convirtieron en eventos regulares, donde se discutían los avances científicos y se recordaban las historias antiguas.
El anciano, aunque ya mayor, seguía compartiendo sus sabidurías con entusiasmo, sintiendo orgullo por el camino que su discípulo había tomado.
El pueblo, que antes era tranquilo, se convirtió en un centro de aprendizaje y exploración, atrayendo a visitantes de lugares lejanos.
El legado del anciano y el joven astrónomo perduró a través de las generaciones, inspirando a otros a explorar los misterios del cosmos.
Así, en ese rincón remoto, el conocimiento de las estrellas continuó brillando, guiando a quienes buscaban entender el vasto cosmos que nos rodea."""

""" La informática es una habilidad esencial en el mundo moderno.
Permite automatizar tareas y aumentar la eficiencia.
Los programadores pueden resolver problemas complejos mediante algoritmos.
La programación fomenta el pensamiento lógico y crítico.
Existen numerosos lenguajes de programación, cada uno con sus funciones específicas.
Python es popular por su simplicidad y adaptabilidad.
Java se utiliza ampliamente en aplicaciones empresariales y móviles.
JavaScript es fundamental para el desarrollo web interactivo.
La programación también se aplica en la análisis de datos y la inteligencia artificial.
Aprender a programar puede abrir muchas oportunidades laborales.
La colaboración en proyectos de programación es común en la tecnología.
Las comunidades de código abierto fomentan el aprendizaje y el desarrollo de ideas.
La programación ayuda a crear herramientas que mejoran la vida cotidiana.
La seguridad informática es un aspecto crítico en el desarrollo de software.
Los programadores deben estar al tanto de las últimas tendencias tecnológicas.
La documentación es clave para el mantenimiento del código a largo plazo.
La práctica constante es fundamental para mejorar las habilidades de programación.
Los errores en el código son comunes, y aprender a depurarlos es esencial.
La programación se puede aprender a través de cursos en línea y plataformas.
Al final, la programación es una forma de creatividad y autoexpresión personal."""

# 3b76f56636d77d62b028acbecea5da3732d2d3f04f19e56adea74f026104bd9e
# 3b76f56636735706347fe516e40db92c9f05a7ad811876e87b0e1530b403a31d

if "__main__" == __name__:
    do()
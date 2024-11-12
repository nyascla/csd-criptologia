import math

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


def reduce_hex_with_multiplication(hex_str, n):
    # Convertir el valor hexadecimal a decimal
    decimal_value = int(hex_str, 16)

    # Definir un factor de multiplicación, para hacer la reducción más variada
    multiplication_factor = 3

    # Multiplicar el valor decimal por el factor y luego aplicar el mapeo modular
    multiplied_value = decimal_value * multiplication_factor
    max_value = 10 ** n - 1
    reduced_value = multiplied_value % (max_value + 1)

    # Devolver el valor como una cadena de longitud n con ceros a la izquierda si es necesario
    return f"{reduced_value:0{n}d}"


def reduce_hex_with_bit_manipulation(hex_str, n):
    # Convertir el valor hexadecimal a decimal
    decimal_value = int(hex_str, 16)

    # Realizar una operación de desplazamiento de bits (shift) para dispersar el valor
    shifted_value = (decimal_value ^ (
                decimal_value >> 3)) & 0xFFFFFFFFF  # Usamos una máscara para mantener los bits relevantes

    # Mapeo modular para asegurar que esté dentro del rango de n dígitos
    max_value = 10 ** n - 1
    reduced_value = shifted_value % (max_value + 1)

    # Formatear el número con ceros a la izquierda si es necesario
    return f"{reduced_value:0{n}d}"

def reduce_hex_rotate(hex_str, n, rotate_by=3):
    # Rotar la cadena
    rotated_hex_str = hex_str[rotate_by:] + hex_str[:rotate_by]
    # Convertir a decimal
    decimal_value = int(rotated_hex_str, 16)
    # Mapeo modular
    max_value = 10 ** n - 1
    reduced_value = decimal_value % (max_value + 1)
    return f"{reduced_value:0{n}d}"

def reduce_hex_with_string_manipulation(hex_str, n):
    # Asegurarnos de que la longitud del valor hexadecimal sea suficiente
    hex_str = hex_str.ljust(len(hex_str) + (len(hex_str) % 2), '0')  # Añadimos ceros si es necesario

    # Realizar una rotación de los caracteres en la cadena hexadecimal
    rotated_str = hex_str[1:] + hex_str[0]  # Rotación simple de un carácter a la izquierda

    # Convertir la cadena rotada a un valor decimal
    rotated_decimal_value = int(rotated_str, 16)

    # Realizamos un mapeo modular para asegurar que el valor esté dentro del rango de n dígitos
    max_value = 10 ** n - 1
    reduced_value = rotated_decimal_value % (max_value + 1)

    # Formatear el valor con ceros a la izquierda si es necesario
    return f"{reduced_value:0{n}d}"

def reduce_hex_sqrt(hex_str, n):
    decimal_value = int(hex_str, 16)
    # Calcula la raíz cuadrada y luego la convierte en entero
    sqrt_value = int(decimal_value ** 0.5)
    # Mapeo modular
    max_value = 10 ** n - 1
    reduced_value = sqrt_value % (max_value + 1)
    return f"{reduced_value:0{n}d}"

def reduce_hex_to_decimal(hex_str, n):
    # Convertir la cadena hexadecimal en un número decimal
    decimal_value = int(hex_str, 16)

    # Mezclar el valor con una operación aritmética para aumentar la dispersión
    mixed_value = (decimal_value * 37 + 41) % (10 ** n)  # Multiplicación por 37 y suma de 41 para dispersar

    # Devolver el valor reducido y formateado con ceros a la izquierda
    return f"{mixed_value:0{n}d}"

def reduce_hex_sin(hex_str, n):
    decimal_value = int(hex_str, 16)
    # Calcula el seno y toma el valor absoluto
    sin_value = abs(math.sin(decimal_value)) * (10 ** n)
    # Convierte a entero
    reduced_value = int(sin_value) % (10 ** n)
    return f"{reduced_value:0{n}d}"


def reduce_hex_to_decimal_v2(hex_str, n):
    # Convertir la cadena hexadecimal en un número decimal
    decimal_value = int(hex_str, 16)

    # Realizar una operación aritmética para aumentar la dispersión
    mixed_value = (decimal_value * 61 + 23) % (10 ** n)  # Multiplicación por 61 y suma de 23

    # Devolver el valor reducido y formateado con ceros a la izquierda
    return f"{mixed_value:0{n}d}"


def reduce_hex_power_mod(hex_str, n, power=3):
    # Divide la cadena en partes de dos caracteres y convierte a decimal
    parts = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    # Eleva cada parte a la potencia especificada y suma los resultados
    powered_sum = sum(part ** power for part in parts)
    # Mapeo modular
    max_value = 10 ** n - 1
    reduced_value = powered_sum % (max_value + 1)
    return f"{reduced_value:0{n}d}"

R = [
    reduce_hex_to_n_digits,
    reduce_hex_with_multiplication,
    reduce_hex_with_bit_manipulation,
    reduce_hex_rotate,
    reduce_hex_with_string_manipulation,
    reduce_hex_sqrt,
    reduce_hex_sin,
    reduce_hex_power_mod,
    reduce_hex_to_decimal,
    reduce_hex_to_decimal_v2
]


def generador_funciones_reduccion_inv():
    index = 1
    while True:
        if index > 10:
            index = 1

        print(f"VUELTA {index}")
        for funcion in R[-index:]:
            yield funcion

        index += 1


def generador_funciones_reduccion():
    while True:
        for funcion in R:
            yield funcion

reduccion = generador_funciones_reduccion()



inv = generador_funciones_reduccion_inv()

if __name__ == "__main__":
    h = "7e49aa4661"
    p = "013039"

    #
    # for i in range(20):
    #     funcion_reduccion = next(inv)
    #     print(funcion_reduccion.__name__)




# 775201
# 000536
# 000186
# 117796
# 000027
# 736479
# 067434
# 357361
# 000107
# 558066


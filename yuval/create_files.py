def add_space_to_lines(input_file, output_file, n):
    # Abrir el archivo de entrada en modo de lectura
    with open(input_file, 'r') as infile:
        # Abrir el archivo de salida en modo de escritura
        with open(output_file, 'w') as outfile:
            # Iterar sobre cada línea del archivo de entrada
            for line in infile:
                # Añadir un espacio al final de la línea y escribirla en el archivo de salida
                spaces = ' ' * n
                outfile.write(line.rstrip() + spaces + '\n' )

# input_path = 'yuval/blanco/blanco.txt'
# output_path = f'yuval/blanco/variations/blanco{n}.txt'
#
# input_path = 'yuval/negro/negro.txt'
# output_path = f'yuval/negro/variations/negro{n}.txt'

for n in range(1,10):
    input_path = 'yuval/blanco/blanco.txt'
    output_path = f'yuval/blanco/variations/blanco{n}.txt'
    add_space_to_lines(input_path, output_path, n)
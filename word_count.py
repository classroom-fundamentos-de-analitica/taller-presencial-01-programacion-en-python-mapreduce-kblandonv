#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#

import glob
import fileinput
def load_input(input_directory):
    """
    Load input files from the specified directory.

    Args:
        input_directory (str): The directory path containing the input files.

    Returns:
        list: A list of tuples, where each tuple contains the filename and a line from the file.
    """
    filenames = glob.glob(input_directory + '/*.*')
    sequence = []
    with fileinput.input(files=filenames) as f:
        for line in f:
            sequence.append((f.filename(), line))
    return sequence


#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
    """
    Maps each word in the input sequence to a key-value pair of (word, 1).

    Args:
        sequence (list): The input sequence of lines.

    Returns:
        list: A new sequence of key-value pairs, where each key is a word and the value is 1.
    """
    new_sequence = [(word.lower().replace(".","").replace(",",""), 1) for _, line in sequence for word in line.split()]
    return new_sequence



#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """
    Sorts the given sequence based on the first element of each item.

    Args:
        sequence (list): The sequence to be sorted.

    Returns:
        list: The sorted sequence.
    """
    sequence = sorted(sequence, key=lambda x: x[0])
    return sequence


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
from itertools import groupby
def reducer(sequence):
    """
    Reduces the sequence by grouping elements with the same key and summing their values.

    Args:
        sequence (list): The input sequence to be reduced.

    Returns:
        list: The reduced sequence with grouped elements and summed values.
    """
    new_sequence = []
    for k, g, in groupby(sequence, lambda x: x[0]):
        key = k
        value =  sum(x[1] for x in g)
        new_sequence.append((key, value))
    return new_sequence


#
# Escriba la función create_ouptput_directory que recibe un nombre de directorio
# y lo crea. Si el directorio existe, la función falla.
#
import os
def create_ouptput_directory(output_directory):
    """
    Creates a new directory for the output files.

    Args:
        output_directory (str): The path of the output directory.

    Raises:
        Exception: If the directory already exists.

    Returns:
        None
    """
    if os.path.isdir(output_directory):
        raise Exception("El directorio ya existe")
    os.mkdir(output_directory)



#
# Escriba la función save_output, la cual almacena en un archivo de texto llamado
# part-00000 el resultado del reducer. El archivo debe ser guardado en el
# directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """
    Save the output sequence to a file in the specified output directory.

    Args:
        output_directory (str): The directory where the output file will be saved.
        sequence (iterable): The sequence of key-value pairs to be written to the file.

    Returns:
        None
    """
    filename = os.path.join(output_directory, "part-00000")
    with open(filename, "w") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """
    Create a marker file in the specified output directory.

    Args:
        output_directory (str): The path to the output directory.

    Returns:
        None
    """
    with open(os.path.join(output_directory, "_SUCCESS"), "w") as f:
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def job(input_directory, output_directory):
    """
    Orchestrates the word count job.

    Args:
        input_directory (str): The path to the input directory.
        output_directory (str): The path to the output directory.

    Returns:
        None
    """
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_ouptput_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":
    job(
        "input",
        "output",
    )

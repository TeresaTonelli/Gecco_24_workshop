import os


def delete_invalid_characters(my_string):
    invalid_characters = [":", ".", ",", " ", ","]
    for character in my_string:
        if character in invalid_characters:
            my_string = my_string.replace(character, "_")
    return my_string


def write_file(file_name, result):
    file_name = delete_invalid_characters(file_name)
    text_file = open(file_name, "a")
    text_file.write(str(result) + "\n")
    text_file.close()


def read_fitness_values(file, n_line):
    element_list = []
    for j in range(n_line):
        fitness_value = file.readline()
        fitness_value = fitness_value.replace("\n", "")
        element_list.append(float(fitness_value))
    return element_list


def create_list_files(directory):
    files = os.listdir(directory)
    return files


def find_element(file, line):
    #file = open(file, "r")
    elements = file.readlines()
    return elements[line - 1]

def write_fitness_file(files_list, line_to_cp, file_name):
    files_list = [open(file, "r") for file in files_list]
    #file_line = open(file_name, "a")
    for file in files_list:
        element = find_element(file, line_to_cp)
        file_line = open(file_name, "a")
        file_line.write(str(element) + "\n")
        file_line.close()
    return file_line

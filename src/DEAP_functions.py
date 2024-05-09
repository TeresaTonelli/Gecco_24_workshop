#Script for the generation of arrays of values of a single candidate solution
#Up to now, this script ONLY works for Kalecki problem

import numpy as np
#from problems.import_data import import_csv_data
#du_dt, t, u, ud = import_csv_data("problems\\kalecki_eqn_case\\datasets")


def compute_points(variable_list):
    m = len(variable_list)
    data_points = []
    for i in range(m):
        #index = dictionary_variables(data_np)[variable_list[i]]
        var_points = [float(x) for x in variable_list[i]]
        data_points = data_points + var_points
    return data_points


def list_division(lista_points, m, i):
    n = len(lista_points)
    l = n // m
    lista = []
    for j in range(m):
        small_list = lista_points[j * l: (j + 1) * l]
        lista = lista + small_list
    return [lista[l * j + i] for j in range(m)]


def from_gen_func_to_array(function, points, m):
    n = len(points) // m
    func_array = np.zeros([n])
    for i in range(n):
        func_array[i] = function(*list_division(points, m, i))
    return func_array
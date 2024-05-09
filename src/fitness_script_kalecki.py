import math
import random
import operator
import numpy as np
import pandas as pd
from deap import gp
from GP_operations import compute_new_u, compute_new_x, compute_new_t, protectedDiv
from GP_methods_kalecki import built_pset_dx
from problems.import_data import *

new_du_dt, new_t, new_u, new_u_d= import_csv_data("problems/kalecki_eqn_case/datasets_1s")


dx_pset = built_pset_dx()
def fitness(candidate_solution):
    candidate_solution = gp.compile(candidate_solution, dx_pset)
    n = len(new_du_dt)
    err = 0
    for i in range(n):
        if type(candidate_solution(new_t, new_u, new_u_d)) == float or type(candidate_solution(new_t, new_u, new_u_d)) == int:
                err += (new_du_dt[i] - candidate_solution(new_t, new_u, new_u_d))**2
        else:
                err += (new_du_dt[i] - candidate_solution(new_t, new_u, new_u_d)[i])**2
        if err > 1e300 or np.isnan(err)[0] == True:
            return 1e300
    return math.sqrt(err / n)


#try_ind = eval("lambda u, ud : operator.sub(operator.mul(0.8, u), operator.mul(1.2, ud))")
#print(fitness(try_ind))

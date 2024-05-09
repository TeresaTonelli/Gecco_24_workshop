from plot_script import plot_fitness_boxplot, plot_fitness_median, plot_fitness_boxplots_series
import os

import pandas as pd
import operator
from GP_methods_kalecki import built_pset_dx
from deap import gp
from DEAP_functions import compute_points, list_division, from_gen_func_to_array
from plot_script import plot_fitness_boxplot, plot_fitness_median, plot_model_derivatives_series
from problems.import_data import import_csv_data

#BOXPLOT 1s 100, 200, 500, 1000 GEN
#fitness_file_list = ["kalecki_files/kalecki_1s_100_gen_fitness_results", "kalecki_files/kalecki_1s_200_gen_fitness_results", "kalecki_files/kalecki_1s_500_gen_fitness_results", "kalecki_files/kalecki_1s_1000_gen_fitness_results"]
#plot_fitness_boxplots_series(fitness_file_list, 30)



#PLOT FOR SOLUTION OF DERIVATIVES: ANALYTIC ONE VS RESULTS --> CASE OF 1 SECOND
new_du_dt, new_t, new_u, new_u_d = import_csv_data("problems/kalecki_eqn_case/datasets_1s")

analytic_derivative = pd.read_csv("problems/kalecki_eqn_case/datasets_1s/du_dt.csv", header=None)
exact_model = from_gen_func_to_array(eval("lambda t, u, ud : operator.sub(operator.mul(0.8, u), operator.mul(1.2, ud))"), compute_points([new_t, new_u, new_u_d]), 3)
file = open("kalecki_files/kalecki_results_individual_1s_1000", "r")
runs_model_list = [from_gen_func_to_array(eval("lambda t, u, ud : " + equation), compute_points([new_t, new_u, new_u_d]), 3) for equation in file.readlines()]
print("len run list", len(runs_model_list))
#runs_model_list = [from_gen_func_to_array(gp.compile(equation, built_pset_dx()), compute_points([new_t, new_u, new_u_d]), 3) for equation in file.readlines()]
plot_model_derivatives_series(analytic_derivative, exact_model, runs_model_list, 30)

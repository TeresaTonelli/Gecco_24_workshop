#Script per fare i plot delle funzioni che ci servono

#quando ho u --> in realtà ho K(t) = 1 - 1.56*t -0.4*t^2 + 0.0533*t^3 +0.0266*t^4
#(torna perchè io i dati i u li ho generati propiro da questa funzione)

#quando ho ud --> in realtà ho K(t-1) = 1 - 1.56*(t-1)- 0.4*(t-1)^2 + 0.0533*(t-1)^3 + 0.0266*(t-1)^4

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from writing_files import read_fitness_values
import seaborn as sns


def plot_derivatives(du_dt_analytic, du_dt_model, name_imm):
    my_t = np.linspace(0, 1, 101)     #(0, 4, 401)
    plt.plot(my_t, du_dt_analytic, 'g', label="exact derivative")
    plt.plot(my_t, du_dt_model, 'm', label="model derivative")
    plt.xlabel("t")
    plt.ylabel("du_dt")
    plt.title("Comparison of derivatives")
    plt.legend(loc="upper left")
    #plt.show()
    plt.savefig("kalecki_plots/" + name_imm + ".png")
    return None



#funzione per i plot della mediana delle fitness di tutti e 30 i run
def plot_fitness_median(files_list, n_gen, exact_fitness):
    files_list = [open(file, "r") for file in files_list]
    m = len(files_list)
    fitness_files_list = []
    for i in range(m):
        fitness_list = read_fitness_values(files_list[i], n_gen-1)
        fitness_files_list.append(fitness_list)
    #in this way fitness_files_list is a list of lists
    #now I compute the medians
    medians = np.zeros(n_gen-1)
    for i in range(n_gen-1):
        median_i = np.median(np.array([fitness_files_list[j][i] for j in range(m)]))
        medians[i] = median_i
    #now I can plot the graph
    plt.plot(np.linspace(1, n_gen-1, n_gen-1), medians)
    plt.axhline(y=exact_fitness, xmin=0.0, xmax=1.0, color = "red", linestyle="--")
    plt.savefig("kalecki_fitness_median_behaviour/fitness_mod_median_30_runs.png")
    return None


def plot_fitness_boxplot(fitness_file, n_gen):
	fitness_file = open(fitness_file, "r")
	fitness_list = read_fitness_values(fitness_file, n_gen-1)
	plt.boxplot(fitness_list)
	plt.title("Boxplot of best individuals' fitness")
	plt.savefig("kalecki_boxplots/boxplot_of_best_fitness_mod.png")
	return None
	

def plot_fitness_boxplots_series(fitness_file_list, n_run):
    fitness_file_list = [open(fitness_file, "r") for fitness_file in fitness_file_list]
    fitness_values_list = []
    for fitness_file in fitness_file_list:
        fitness_values = read_fitness_values(fitness_file, n_run)
        fitness_values_list.append(fitness_values)
    sns.set_theme(context='paper', style='white', font='serif', font_scale=1.2,
              color_codes=True, rc=None)
    runs_labels = ["100", "200", "500", "1000"]   
    plt.boxplot(fitness_values_list, labels=runs_labels, showmeans = True, meanline = True)
    #ora dobbiamoaggiungere la linea spezzata di decrescita della media tra i vari boxplot
    #calcoliamo la mediana
    median_fitness = [np.median(np.array(fitness_values)) for fitness_values in fitness_values_list]
    #facciamo il grafico
    plt.plot(np.arange(1, len(runs_labels) + 1), median_fitness, color="orange", linestyle="solid", marker="o", label="Median")
    #calcoliamo la media
    mean_fitness = [np.mean(np.array(fitness_values)) for fitness_values in fitness_values_list]
    #facciamo il grafico
    plt.plot(np.arange(1, len(runs_labels) + 1), mean_fitness, color="g", linestyle="solid", marker="o", label="Mean")
    #add labels
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="upper right")
    plt.savefig("kalecki_boxplots/boxplot_of_best_fitness_wrt_increasing_runs_1s_line_11.svg")
    return None


def plot_model_derivatives_series(analytic_derivative, exact_model, runs_model_list, n_gen):
    sns.set_theme(context='paper', style='white', font='serif', font_scale=1.2,
              color_codes=True, rc=None)
    x_axis = np.linspace(0, 1, 101)   
    #plot each runned model
    for i in range(0, 1):
        plt.plot(x_axis, runs_model_list[i], color="green", label="Single GP individual", alpha = 0.1)
    for i in range(1, len(runs_model_list)):
        plt.plot(x_axis, runs_model_list[i], color="green", alpha = 0.1)   #alpha dovrebbe regolare la trasparenza dei plot
    # now I compute the medians
    medians = np.zeros(101)
    for i in range(101):
        median_i = np.median(np.array([runs_model_list[j][i] for j in range(len(runs_model_list))]))
        print("median i", median_i)
        medians[i] = median_i
    # now I can plot the graph
    plt.plot(x_axis, exact_model, color="blue", label="Kalecki's model")
    plt.plot(x_axis, analytic_derivative, color="red", linestyle = "dashed", label="Keller derivative's approximation")
    plt.plot(x_axis, medians, color=(0.2, 0.8, 0.3), label="Median of GP individuals")
    plt.xlabel("t")
    plt.ylabel("K'(t)")
    plt.legend(loc="upper right")
    plt.savefig("kalecki_plot_solutions/total_derivatives_comparison_1s_1000_copy_camera_ready.svg")
    return None

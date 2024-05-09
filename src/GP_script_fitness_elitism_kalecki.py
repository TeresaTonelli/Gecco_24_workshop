import random
import pandas as pd
from GP_methods_kalecki import *
from fitness_script_kalecki import fitness, dx_pset, new_t, new_u, new_u_d
from joblib import Parallel, delayed
import datetime
from writing_files import delete_invalid_characters, write_file
from plot_script import plot_derivatives
from DEAP_functions import compute_points, list_division, from_gen_func_to_array

def gp_algorithm_elitism(fitness, pop_size, p_m, p_cross, n_iter, pset_sx, pset_dx, n_min, n_max, tournsize):
    init_pop = init_population(pop_size, pset_sx, pset_dx, n_min, n_max)
    pop = init_pop
    best = pop[0]
    #aggiungo i due file in cui salverò fitness e individui migliori
    name_file = str(datetime.datetime.utcnow())
    fitness_file = "kalecki_files/fitness_files_1s_1000_gen/fitness_file" + name_file   
    individual_file = "kalecki_files/individual_files_1s_1000_gen/individual_file" + name_file  
    for i in range(n_iter):
        fitnessess = Parallel(n_jobs = 10, backend="loky")(delayed(fitness)(ind) for ind in pop)
        tuple = [(pop[i], fitnessess[i]) for i in range(len(pop))]
        selected = tournament_selection_tuples(tuple, pop, tournsize)
        pop = selected
        offsprings = pop
        for j in range(len(pop) // 2):
            p = random.uniform(0, 1)
            if p < p_cross:
                i_1, i_2 = random.choices(range(pop_size), k=2)
                ind_1 = offsprings[i_1]  
                ind_2 = offsprings[i_2]   
                of_1, of_2 = crossover_sx(ind_1, ind_2)
                of_1, of_2 = crossover_dx(of_1, of_2)
                offsprings[i_1] = of_1   
                offsprings[i_2] = of_2  
        offsprings = sample_mutation(p_m, [mutation_uniform, mutation_subtree,
                                           mutation_ephemeral, mutation_node_replacement, mutation_shrink], offsprings, pset_dx)
        print("i", i)
        for j in range(len(offsprings)):
        	if len(offsprings[j]) > 4:
                	offsprings[j] = cut_tree(offsprings[j], 4, pset_sx)
        #candidate_best = min(offsprings, key=fitness)
        #ora devo ricalcolare le nuove fitness degli offspring
        off_fitnessess = Parallel(n_jobs = 10, backend="loky")(delayed(fitness)(ind) for ind in offsprings)
        candidate_best = compute_min_fitness_ind(offsprings, off_fitnessess)
        candidate_worst = compute_max_fitness_ind(offsprings, off_fitnessess)
        f = fitness(candidate_best)
        fb = fitness(best)
        #ora trascrivo i risultati nei corrispettivi file --> devo già trascrivere il migliore tra best e candidate best
        if i < n_iter - 1:
            if f < fb:
                write_file(fitness_file, fitness(candidate_best))
                write_file(individual_file, candidate_best)
            else:
                write_file(fitness_file, fitness(best))
                write_file(individual_file, best)
        else:
            write_file(fitness_file, "final_population")
            write_file(individual_file, "final_population")
            for l in range(pop_size):
                write_file(fitness_file, off_fitnessess[l])
                write_file(individual_file, offsprings[l])
        # qua bisogna inserire l'elitismo
        offsprings.remove(candidate_worst)
        offsprings.append(best)
        if f < fb:
            best = candidate_best
        if fb == 0:
            return best
        ##qua bisogna inserire l'elitismo
        #offsprings.remove(candidate_worst)
        #offsprings.append(best)
        pop = offsprings
    print("best and its fitness", best, fitness(best))
    write_file("kalecki_files/kalecki_results_individual_1s_1000", best)
    write_file("kalecki_files/kalecki_results_fitness_1s_1000", fitness(best))       
    #generate the plot of derivatives
    du_dt_model = from_gen_func_to_array(gp.compile(best, dx_pset), compute_points([new_t, new_u, new_u_d]), 3)
    du_dt_analytic = pd.read_csv("problems/kalecki_eqn_case/datasets_1s/du_dt.csv", header=None)
    plot_derivatives(du_dt_analytic, du_dt_model, delete_invalid_characters(name_file))
    return best



sx_pset = built_pset_sx()
best = gp_algorithm_elitism(fitness, 500, 0.2, 0.8, 1000, sx_pset, dx_pset, 1, 3, 3)

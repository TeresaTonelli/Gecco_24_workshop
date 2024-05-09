from writing_files import *


#directory = "kalecki_files/fitness_files_mod_100_gen/"
#fitness_file_list = os.listdir(directory)
#fitness_file_list = [directory + fitness_file_list[i] for i in range(len(fitness_file_list))]

#write_fitness_file(fitness_file_list, 75, "kalecki_files/kalecki_mod_75_gen_fitness_results")

directory = "kalecki_files/individual_files_mod_100_gen/"
fitness_file_list = os.listdir(directory)
fitness_file_list = [directory + fitness_file_list[i] for i in range(len(fitness_file_list))]

write_fitness_file(fitness_file_list, 99, "kalecki_files/kalecki_mod_100_gen_individual_results")

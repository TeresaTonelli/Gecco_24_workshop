# Gecco_24_workshop
This repository contains the code for the reconstruction of Kalecki's model through genetic programming, as proposed in the student workshop "Genetic Programming for the Reconstruction of Delay Differential Equations in Economics".  

The GP algorithm is implemented through 3 scripts: "GP_methods_kalecki.py", "fitness_script_kalecki.py" and "GP_script_fitness_elitism_kalecki.py": in the first one, all the genetic operators are defined, in the second the fitness function is implemented and in the last one the algorithm is developed using previous fitness function and operators.   
In the script "GP_script_fitness_elitism_kalecki.py" the code for GP evolution is provided, and running it the user will obtain two different text files with respectively all the best fitness and best individual for each iteration; they are contained in the "kalecki_files" directory, in fitness and individual folder respectively.   
The first time this script is run, it also creates 2 files, which save the best individual of the entire algorithm and its fitness. For all 30 runs, this files will be updated adding the best individual and fitness of each specific run.   
Moreover, each run also generates a plot of the best individual, which compares its behavior with the one of Keller's approximation, saved in the "kalecki_plots" folder.  

To generate the plots provided in the paper, it is sufficient to run the "plot_main.py" file. The script automatically runs the comparison between the exact model, Keller's approximation, and GP results: if the user wants to obtain boxplots, it is sufficient to de-comment the first part of the script. It is important to underline a small modification carried on to the file of individual results: to obtain a valid code, the strings representing the best individuals have been modified, replacing each operation (for example "add") with operator.operation (for example operator.add).   
These plots are saved in the "kalecki_boxplots" folder and in the "kalecki_plot_solutions" folder respectively.   

It is important to underline that to run the entire code a specific environment has been used, whose packages are contained in ... .

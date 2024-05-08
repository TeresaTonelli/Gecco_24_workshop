# Gecco_24_workshop
This repository contains the code for the reconstruction of Kalecki's model through genetic programming, as proposed in the student workshop "Genetic Programming for the Reconstruction of Delay Differential Equations in Economics".   
In the script "GP_scripts.py" the code for GP evolution is provided, and running it the user will obtain two different text files with respectively all the best fitness and best individual for each iteration; they are contained in the "kalecki_files" directory, in fitness and individual folder respectively.   
The first time this script is run, it also creates 2 files, which save the best individual of the entire algorithm and its fitness. For all 30 runs, this files will be updated adding the best individual and fitness of each specific run.   
Moreover, each run also generates a plot of the best individual, which compares its behavior with the one of Keller's approximation, saved in the "kalecki_plots" folder.  

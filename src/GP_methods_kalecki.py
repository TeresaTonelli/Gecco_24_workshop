import copy
import deap.tools
from deap import gp
from deap.gp import MetaEphemeral

from GP_operations import *
from mut_uniform_script import mutUniform
from mut_node_replacement_script import mutNodeReplacement


def built_pset_sx():
    pset = gp.PrimitiveSet("", 2)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addEphemeralConstant("eph_cost_sx", lambda: random.choice([round(0.1*l, 1) for l in range(-20, 20)]))
    pset.renameArguments(ARG0= "t")
    pset.renameArguments(ARG1="u")
    return pset


def built_pset_dx():
    pset = gp.PrimitiveSet("", 3)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addEphemeralConstant("eph_cost_dx", lambda: random.choice([round(0.1*l, 1) for l in range(-20, 20)]))
    pset.renameArguments(ARG0="t")
    pset.renameArguments(ARG1="u")
    pset.renameArguments(ARG2="ud")
    return pset



def built_tree(pset_sx, pset_dx, n_min, n_max):
    list_1 = gp.genHalfAndHalf(pset_sx, n_min, n_max)
    list_2 = gp.genHalfAndHalf(pset_dx, n_min, n_max)
    my_add = deap.gp.Primitive("add", (float, float), float)
    final_list = [my_add] + list_1 + list_2
    final_tree = gp.PrimitiveTree(final_list)
    return final_tree


def generate_tree(root, sx_subtree, dx_subtree):
    list_sx = list(sx_subtree)
    list_dx = list(dx_subtree)
    my_root = root
    final_list = [my_root] + list_sx + list_dx
    final_tree = gp.PrimitiveTree(final_list)
    return final_tree


def init_population(n_pop, pset_sx, pset_dx, n_min, n_max):
    pop = []
    for i in range(n_pop):
        individual = built_tree(pset_sx, pset_dx, n_min, n_max)
        pop.append(individual)
    return pop


def tournament_selection(fit, pop, tournsize):
    n = len(pop)
    selected = []
    for i in range(n):
        tournament = random.choices(pop, k=tournsize)
        sel_ind = min(tournament, key=fit)
        selected.append(sel_ind)
    return selected


def tournament_selection_dictionary(dictionary, pop, tournsize):
	n = len(pop)
	selected = []
	for i in range(n):
		individuals = dictionary.keys()
		tournament = random.choices(pop, k=tournsize)
		fitnesses = [dictionary[ind] for ind in individuals]
		min_fit = min(fitnesses)
		min_ind = [ind for ind in individuals if dictionary[ind] == min_fit][0]
		selected.append(min_ind)
	return selected



def tournament_selection_tuples(tuple, pop, tournsize):
        n = len(pop)
        selected = []
        for i in range(n):
                tournament = random.choices(range(n), k=tournsize)
                individuals = [tuple[j][0] for j in range(n)]
                fitnesses = [tuple[j][1] for j in range(n)]
                sel_ind = [copy.deepcopy(individuals[k]) for k in tournament]
                sel_fit = [fitnesses[k] for k in tournament]
                min_index = np.argmin(np.array(sel_fit))
                best_ind = sel_ind[min_index]
                selected.append(best_ind)
        return selected



def mutation_subtree(individual, pset):
    index = random.randint(1, len(individual) - 1)
    mut_slice = individual.searchSubtree(index)
    new_subtree = gp.PrimitiveTree(gp.genHalfAndHalf(pset, 1, 2))
    individual[mut_slice] = new_subtree
    return individual


def mutation_uniform(individual, pset):
    return mutUniform(individual, pset)[0]


def mutation_node_replacement(individual, pset):
    return mutNodeReplacement(individual, pset)[0]

def mutation_ephemeral(individual, pset):
    mode = "all"
    return deap.gp.mutEphemeral(individual, mode)[0]


def mutation_shrink(individual, pset):
    return deap.gp.mutShrink(individual)[0]


def sample_mutation(p_m, mutation_list, pop, pset):
    for i in range(len(pop)):
        p = random.random()
        if p < p_m:
            my_mutation = random.choice(mutation_list)
            pop[i] = my_mutation(pop[i], pset)
    return pop


def compute_subtrees(tree):
    sx_slice = tree.searchSubtree(1)
    sx_subtree = tree[sx_slice]
    m_sx = len(sx_subtree)
    m_dx = m_sx + 1
    return 1, m_dx


def crossover(ind_1, ind_2):
    return gp.cxOnePoint(ind_1, ind_2)


def crossover_sx(ind_1, ind_2):
    m_sx_1 = compute_subtrees(ind_1)[0]
    m_sx_2 = compute_subtrees(ind_2)[0]
    m_dx_1 = compute_subtrees(ind_1)[1]
    m_dx_2 = compute_subtrees(ind_2)[1]
    slice_sx_1 = ind_1.searchSubtree(m_sx_1)
    slice_sx_2 = ind_2.searchSubtree(m_sx_2)
    slice_dx_1 = ind_1.searchSubtree(m_dx_1)
    slice_dx_2 = ind_2.searchSubtree(m_dx_2)
    subtree_sx_ind_1 = gp.PrimitiveTree(ind_1[slice_sx_1])
    subtree_sx_ind_2 = gp.PrimitiveTree(ind_2[slice_sx_2])
    subtree_dx_ind_1 = gp.PrimitiveTree(ind_1[slice_dx_1])
    subtree_dx_ind_2 = gp.PrimitiveTree(ind_2[slice_dx_2])
    subtree_cx_1, subtree_cx_2 = gp.cxOnePoint(subtree_sx_ind_1, subtree_sx_ind_2)
    cx_ind_1 = generate_tree(deap.gp.Primitive("add", (float, float), float),subtree_cx_1, subtree_dx_ind_1)
    cx_ind_2 = generate_tree(deap.gp.Primitive("add", (float, float), float), subtree_cx_2, subtree_dx_ind_2)
    return cx_ind_1, cx_ind_2


def crossover_dx(ind_1, ind_2):
    m_sx_1 = compute_subtrees(ind_1)[0]
    m_sx_2 = compute_subtrees(ind_2)[0]
    m_dx_1 = compute_subtrees(ind_1)[1]
    m_dx_2 = compute_subtrees(ind_2)[1]
    slice_sx_1 = ind_1.searchSubtree(m_sx_1)
    slice_sx_2 = ind_2.searchSubtree(m_sx_2)
    slice_dx_1 = ind_1.searchSubtree(m_dx_1)
    slice_dx_2 = ind_2.searchSubtree(m_dx_2)
    subtree_sx_ind_1 = gp.PrimitiveTree(ind_1[slice_sx_1])
    subtree_sx_ind_2 = gp.PrimitiveTree(ind_2[slice_sx_2])
    subtree_dx_ind_1 = gp.PrimitiveTree(ind_1[slice_dx_1])
    subtree_dx_ind_2 = gp.PrimitiveTree(ind_2[slice_dx_2])
    subtree_cx_1, subtree_cx_2 = gp.cxOnePoint(subtree_dx_ind_1, subtree_dx_ind_2)
    cx_ind_1 = generate_tree(deap.gp.Primitive("add", (float, float), float), subtree_sx_ind_1, subtree_cx_1)
    cx_ind_2 = generate_tree(deap.gp.Primitive("add", (float, float), float), subtree_sx_ind_2, subtree_cx_2)
    return cx_ind_1, cx_ind_2


def compute_len_subtrees(tree):
    n = len(tree)
    e = np.zeros(n)
    for i in range(n):
        end = i + 1
        total = list(tree)[i].arity
        while total > 0:
            total += list(tree)[end].arity - 1
            end += 1
        e[i] = end
    return list(e)

def compute_arities(tree):
    n = len(tree)
    arities = np.zeros(n)
    for i in range(n):
        arities[i] = list(tree)[i].arity
    return list(arities)



def compute_levels_2(e, arities):
    n = len(e)
    levels = np.zeros(n)
    counter = 0
    lev = 0
    void_index = list(np.arange(1, n+1))
    begin = 1
    level = 1
    while len(void_index) > 0 and begin < n:
        levels[begin] = level
        void_index.remove(begin)
        end = 0
        partial_list = []
        while end < n:
            end = begin + 1
            total = arities[begin]
            while total > 0:
                total += arities[end] - 1
                end += 1
            ee = end
            while end not in void_index:
                end = end + 1
                ee = end
            partial_list.append(ee)
            begin = end
        for j in partial_list[:-1]:
            if levels[j] == 0:
                levels[j] = level
        for j in partial_list[:-1]:
            if j in void_index:
                void_index.remove(j)
        level += 1
        if len(void_index) > 0:
            begin = min(void_index)
        else:
            break
    return levels


def compute_dictionary_e_a(e, arities):
    dic = {}
    for i in range(len(e)):
        if e[i] not in dic:
            tmp_list = [[i, arities[i]]]
            for j in range(i+1, len(e)):
                if e[j] == e[i]:
                    tmp_list.append([j, arities[j]])
            dic[e[i]] = tmp_list
    return dic


def cut_tree(tree, d, pset):
    tree_list = list(tree)
    n = len(tree)
    D = tree.height
    e = compute_len_subtrees(tree)
    arities = compute_arities(tree)
    dic = compute_dictionary_e_a(e, arities)
    levels = list(compute_levels_2(e, arities))
    for i in range(n-1, 0, -1):
        if levels[i] > d:
            tree_list.pop(i)
            arities.pop(i)
            levels.pop(i)
    for i in range(len(levels)):
        if levels[i] == d and arities[i] > 0:
            #r = random.choice([round(0.1*l, 1) for l in range(-20, 20)])
            #tree_list[i] = gp.Terminal(r, str(r), float)
            node = tree[i]
            term = random.choice(pset.terminals[node.ret])
            if type(term) is MetaEphemeral:
                term = term()
            tree_list[i] = term
    return gp.PrimitiveTree(tree_list)


def compute_min_fitness_ind(pop, fitnesses):
    min_index = np.argmin(np.array(fitnesses))
    min_ind = pop[min_index]
    return min_ind


def compute_max_fitness_ind(pop, fitnesses):
    max_index = np.argmax(np.array(fitnesses))
    max_ind = pop[max_index]
    return max_ind

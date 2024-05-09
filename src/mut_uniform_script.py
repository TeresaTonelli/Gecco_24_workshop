import random
from deap import gp


def mutUniform(individual, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.

    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :returns: A tuple of one tree.
    """
    index = random.randrange(len(individual))
    #print(index)
    slice_ = individual.searchSubtree(index)
    #print(slice_)
    type_ = individual[index].ret
    #print(type_)
    individual[slice_] = gp.PrimitiveTree(gp.genHalfAndHalf(pset, 1, 2))
    #print(individual)
    return individual,


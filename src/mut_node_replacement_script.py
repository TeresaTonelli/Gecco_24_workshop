import random
from deap import gp


def mutNodeReplacement(individual, pset):
    """Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.

    :param individual: The normal or typed tree to be mutated.
    :returns: A tuple of one tree.
    """
    if len(individual) < 2:
        return individual,

    index = random.randrange(1, len(individual))
    node = individual[index]

    if node.arity == 0:  # Terminal
        return individual,
    else:  # Primitive
        prims = [p for p in pset.primitives[node.ret] if p.args == node.args]
        individual[index] = random.choice(prims)

    return individual,

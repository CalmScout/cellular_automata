"""
Contains useful auxiliary functions.
"""
import numpy as np
import string
import random
import pickle


def cartesian_product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generates random string.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def save_obj(obj, path, name):
    """
    Saves :param obj to fie located at :param path with the name :param name
    """
    with open(path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_obj(path, name):
    """
    Loads file with name :param path, with the name :param name
    """
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def generate_rules_rand_1d_no_memory(ca):
    """
    Generates dictionary of rules and save it to file.
    """
    cell_states_arr = np.array(range(ca.num_of_cell_states))
    # number of cells in the neighborhood configuration
    n = 2 * ca.neighb_radius + 1
    # temporary array for all vectors of which we want to compute cartesian product
    my_arr = []
    for i in range(n):
        my_arr.append(cell_states_arr)
    my_arr = np.array(my_arr)
    # all neighborhoods
    neighb_all = cartesian_product(*my_arr)
    ca.rules = {}
    for i in range(len(neighb_all)):
        # generate new random state for center cell of the neighbourhood
        new_state = np.random.randint(low=0, high=ca.num_of_cell_states, dtype=np.int16)
        # remove brackets '[' and ']'
        ca.rules[str(neighb_all[i])[1:-1]] = new_state
    # save dictionary to file for further comparison with identified rules
    ca.id_str = id_generator()
    save_obj(ca.rules, path='data/no_memory/', name=ca.id_str)


def nth_term(generator, n):
    """ Returns the nth term of an infinite generator. """
    for i, x in enumerate(generator):
        if i == n - 1:
            return x

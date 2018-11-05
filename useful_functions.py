"""
Contains useful auxiliary functions.
"""
import numpy as np
import string
import random
import pickle

def cartesian_product(*arrays):
    """
    Fast cartesian product implementation.
    """
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[..., i] = a
    return arr.reshape(-1, la)


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

"""
Contains classes for CA identification.
"""
import numpy as np
from constants import data_path_no_memory
from useful_functions import load_obj

rules = load_obj(data_path_no_memory, "L2I5ZK")
print(rules)
# define our space of rules where we would be doing a search

"""
Contains constants for data generation and identification.
"""
data_path = "data/"

# Constants for Wolfram's rule
data_path_wolfram = data_path + "wolfram/"
size_wolfram = 100
steps_wolfram = 100
prob_of_ones_tpl_wolfram = (0.05, 0.3, 0.5, 0.7, 0.95)

# Constants for generators of CA without memory
data_path_no_memory = data_path + "no_memory/"
size_no_memory = 200
steps_no_memory = 200
neighb_radius_no_memory = 4    # neighbourhood radius we will use in 1D CA
max_neighb_radius = 10
num_of_cell_states = 4   # number of states in which can be each cell
max_num_of_cell_states = 10

# Constants for generators of CA with memory
data_path_with_memory = data_path + "with_memory/"

"""
Contains constants for data generation and identification.
"""
data_path = "data/"

# Constants for generators of CA without memory
data_path_no_memory = data_path + "no_memory/"

# Constants for generators of CA with memory
data_path_with_memory = data_path + "with_memory/"

# Constants common for CA with memory and CA without memory
# Constants for CA evolution
size = 200
steps = 200
# Constants for CA rules generation
neighb_rad = 3    # neighbourhood radius we will use in 1D CA
min_neighb_rad = 1
max_neighb_rad = 10
num_of_cell_states = 4   # number of states in which can be each cell
min_num_of_cell_states = 2
max_num_of_cell_states = 10

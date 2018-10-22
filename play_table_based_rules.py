"""
Simple rule-based CA implementation.
"""
import numpy as np
import matplotlib.pyplot as plt

rules_table = {
    "000": 1,
    "001": 0,
    "010": 1,
    "011": 1,
    "100": 0,
    "101": 1,
    "110": 1,
    "111": 0
}

NUMBER_OF_CELLS = 100
TIME = 100

for percent in range(0, 101, 5): # percent of receiving '1' not '0' in initial conditions
    grid = np.zeros((NUMBER_OF_CELLS, TIME), dtype=int)

    # initialization
    grid[:, 0] = np.random.randint(low=0, high=100, size=NUMBER_OF_CELLS)
    grid[:, 0] = (grid[:, 0] < percent).astype(int)

    print("Percentage of initialization '1': {}, actual number of '1': {}/{}.".format(percent, np.sum(grid[:, 0]),
                                                                                      NUMBER_OF_CELLS))

    # evolution
    for t in range(1, TIME):
        for idx in range(NUMBER_OF_CELLS - 1):
            neighborhood = str(grid[idx - 1, t - 1]) + str(grid[idx, t - 1]) + str(grid[idx + 1, t - 1])
            grid[idx, t] = rules_table[neighborhood]
        # boundary condition idx == NUMBER_OF_CELLS - 1
        idx = NUMBER_OF_CELLS - 1
        neighborhood = str(grid[idx - 1, t - 1]) + str(grid[idx, t - 1]) + str(grid[0, t - 1])
        grid[idx, t] = rules_table[neighborhood]

    plt.pcolormesh(grid)
    plt.savefig('evolution{}.png'.format(percent))

import numpy as np


def convert_to_int(x):
    """ Accepts input, possibly a list, and converts to integer """

    if isinstance(x, list):
        return [int(i) for i in x]
    elif np.isnan(x):
        return 0
    else:
        return int(x)

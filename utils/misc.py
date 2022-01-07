import numpy as np


def convert_to_int(x):
    """ Accepts input, possibly a list, and converts to integer """

    if isinstance(x, list):
        return [int(i) for i in x]
    elif np.isnan(x):
        return 0
    else:
        return int(x)

def convert_to_auid(Auids):
    """ Takes in integer Auid and converts to 'AUTHOR_ID:{}'.format(Auid) """
    
    result = []
    
    for value in Auids:
        if value is None:
            result.append(None)
        else:
            result.append('AUTHOR_ID:{}'.format(value))
    return result
    
"""A DictIterator iterates across all combinations of values of keys."""


def iterateDict(dct):
    """
    Parameters
    ----------
    dct: dictionary whose values are lists

    Returns
    -------
    iterator-dict
    """
    def get(dct, index_dct):
        return {k: dct[k][index_dct[k]] for k in dct.keys()}
    # Initializations
    index_dct = {k: 0 for k in dct.keys()}  # list position for each key
    keys = list(dct.keys()) #  Order in which keys are incremented
    keys.reverse()
    # First value
    yield get(dct, index_dct)
    # Iteration
    done = False
    while not done:
        carry = 1
        for key in keys:
            new_index = index_dct[key] + carry
            if new_index == len(dct[key]):
                index_dct[key] = 0
                carry = 1
            else:
                carry = 0
                index_dct[key] = new_index
                break
        #
        if carry == 0:
            yield get(dct, index_dct)
        else:
            # Have completed iteration
            break

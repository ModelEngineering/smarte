"""A DictIterator iterates across all combinations of values of keys."""


def iterateDict(dct):
    """
    Parameters
    ----------
    dct: dict (dictionary whose values are lists)

    Returns
    -------
    iterator-dict
    """
    def get(dct, index_dct):
        return {k: dct[k][index_dct[k]] for k in dct.keys()}
    # Ensure that dct consists of lists
    new_dct = {}
    for key, value in dct.items():
        # Check for entry is a list
        if isinstance(value, list):
            if not isinstance(value, str):
                new_dct[key] = value
                continue
        # Not a list already
        new_dct[key] = [value]
    # Initializations
    index_dct = {k: 0 for k in new_dct.keys()}  # list position for each key
    keys = list(new_dct.keys()) #  Order in which keys are incremented
    keys.reverse()
    # First value
    yield get(new_dct, index_dct)
    # Iteration
    done = False
    while not done:
        carry = 1
        for key in keys:
            new_index = index_dct[key] + carry
            if new_index == len(new_dct[key]):
                index_dct[key] = 0
                carry = 1
            else:
                carry = 0
                index_dct[key] = new_index
                break
        #
        if carry == 0:
            yield get(new_dct, index_dct)
        else:
            # Have completed iteration
            break

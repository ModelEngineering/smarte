"""Utilities"""


def subsetLabels(labels, max_label):
    """
    Assigns max_label to non-blank, evenly spaced.

    Parameters
    ----------
    labels: list-object (with str repreentation)
    max_label: int
    
    Returns
    -------
    list-str
    """
    labels = list(labels)
    if len(labels) > max_label:
        new_labels = ["" for _ in range(len(labels))]
        incr = len(labels)//max_label
        for idx in range(max_label-1):
            pos = incr*idx
            new_labels[pos] = labels[pos]
        new_labels[-1] = labels[-1]
        labels = new_labels
    return labels

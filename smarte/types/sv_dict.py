"""ElementDict that has a single value for each attribute"""

from smarte.types.elemental_dict import ElementalDict
from smarte.types.elemental_type import isList


class SVDict(ElementalDict):

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict
        """
        super().__init__(**kwargs)
        # Validatation checks
        falses = [isList(v) for v in self.values()]
        if any(falses):
            raise ValueError("Values must be elemental, non-lists: %s" % str(kwargs))

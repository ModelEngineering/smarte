"""A collection of conditions expressed as a hypercube."""


import smarte.constants as cn
from smarte.types.mv_dict_hypercube import MVDictHypercube
from smarte.types.elemental_dict import ElementalDict


class _ElementalConditionCollection(ElementalDict):
    default_dct = {k: [v] for k, v in cn.SD_CONDITION_DCT.items()}


class ConditionCollection(MVDictHypercube):
    default_dct = {k: [v] if v != cn.SD_CONDITION_VALUE_ALL else v
          for k, v in cn.SD_CONDITION_DCT.items()}
    expansion_dct = dict(cn.SD_CONDITION_EXPANSION_DCT)

    def __init__(self, **kwargs):
        self.kwargs = _ElementalConditionCollection(**kwargs)
        super().__init__(**kwargs)

    def __str__(self):
        return str(self.kwargs)

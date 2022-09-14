"""A collection of factor values."""


import smarte.constants as cn
from smarte.types.mv_dict import MVDict


class FactorCollection(MVDict):
    default_dct = {k: [] for k in cn.SD_CONDITION_DCT.keys()}
    expansion_dct = dict(cn.SD_CONDITION_EXPANSION_DCT)

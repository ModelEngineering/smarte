"""A ResultCollection describes the outcomes of a collection of experiments"""


import smarte.constants as cn
from smarte.types.mv_dict_hypercube import MVDictTable


class ResultCollection(MVDictTable):
    default_dct = {k: [] for k in cn.SD_ALL}

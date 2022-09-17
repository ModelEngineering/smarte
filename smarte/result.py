"""A Result specifies the conditions and outcomes of an experiment."""

import smarte.constants as cn
from smarte.types.sv_dict import SVDict


class Result(SVDict):
    default_dct = {k: None if v == cn.SD_CONDITION_VALUE_ALL else v
         for k, v in  cn.SD_ALL_DCT.items()}

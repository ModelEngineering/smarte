"""A Result specifies the conditions and outcomes of an experiment."""

import smarte.constants as cn
from smarte.types.sv_dict import SVDict


class Result(SVDict):
    default_dct = cn.SD_ALL_DCT

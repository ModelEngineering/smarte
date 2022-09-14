"""A Condition is a specification of one level for all factors."""

import smarte.constants as cn
from smarte.types.sv_dict import SVDict


class Condition(SVDict):
    default_dct = cn.SD_CONDITION_DCT

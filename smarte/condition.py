"""A Condition is a specification of one level for all factors."""

import smarte.constants as cn
from smarte.types.sv_dict import SVDict


class Condition(SVDict):
    # Select single values or None if multiple values specified
    default_dct = {k: None if v == cn.SD_CONDITION_VALUE_ALL else v
         for k, v in  cn.SD_CONDITION_DCT.items()}

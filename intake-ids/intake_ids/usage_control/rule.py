from ..ids_information_model.rule import Rule
from ..ids_information_model.prohibition import Prohibition
from ..ids_information_model.permission import Permission
from ..ids_information_model.left_operand import ELAPSED_TIME
from .pattern import *

def get_pattern_by_rule(rule: Rule) -> str:
    if isinstance(rule, Prohibition):
        return PROHIBIT_ACCESS

    if not isinstance(rule, Permission):
        return OTHER_PATTERN

    constraints = rule.constraint
    post_duties = rule.post_duty

    if len(constraints) > 1:
        if len(post_duties) != 0:
            return USAGE_UNTIL_DELETION
        else:
            return USAGE_DURING_INTERVAL
    elif len(constraints) == 1:
        con = constraints[0]
        left_operand = con.left_operand

        if left_operand.id == ELAPSED_TIME.id:
            return DURATION_USAGE
        else:
            return OTHER_PATTERN

    if len(post_duties) == 0:
        return PROVIDE_ACCESS
    
    return OTHER_PATTERN
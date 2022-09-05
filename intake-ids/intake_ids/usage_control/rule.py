import isodate
from datetime import timedelta, datetime
from ..ids_information_model.rule import Rule
from ..ids_information_model.prohibition import Prohibition
from ..ids_information_model.permission import Permission
from ..ids_information_model.typed_literal import TypedLiteral
from ..ids_information_model.left_operand import ELAPSED_TIME
from ..ids_information_model.binary_operator import AFTER, BEFORE
from .pattern import *

def _get_right_operand_value(right_operand: TypedLiteral[str] | str) -> str:
    ret: str = ''
    if isinstance(right_operand, TypedLiteral):
        ret = right_operand.value
    else:
        ret = right_operand
    return ret

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

def get_date(rule: Rule) -> datetime:
    date_str = _get_right_operand_value(rule.constraint[0].right_operand)
    return isodate.parse_datetime(date_str)

def get_duration(rule: Rule) -> timedelta:
    duration_str = _get_right_operand_value(rule.constraint[0].right_operand)
    return isodate.parse_duration(duration_str)

def get_interval(rule: Rule) -> tuple[datetime, datetime]:
    start: datetime
    end: datetime
    for constraint in rule.constraint:
        op = constraint.operator
        if op.id == AFTER.id:
            st_str = _get_right_operand_value(constraint.right_operand)
            start = isodate.parse_datetime(st_str)
        elif op.id == BEFORE.id:
            st_str = _get_right_operand_value(constraint.right_operand)
            end = isodate.parse_datetime(st_str)

    return start, end


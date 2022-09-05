from datetime import datetime
from ..ids_information_model.contract import Contract
from ..ids_information_model.artifact import Artifact
from ..ids_information_model.rule import Rule
from ..ids_information_model.permission import Permission
from ..ids_information_model.action import DELETE
from .exceptions import RuleError, ContractError
from .rule import get_pattern_by_rule, get_duration, get_interval, get_date
from .pattern import *

def validate_contract(contract: Contract):
    validate_contract_dates(contract)

def validate_contract_dates(contract: Contract):
    if datetime.now(contract.contract_end.value.tzinfo) > contract.contract_end.value or datetime.now(contract.contract_start.value.tzinfo) < contract.contract_start.value:
        raise ContractError('Contract is either not in effect yet, or has run out')

def validate_rule(rule: Rule, artifact: Artifact):
    pattern = get_pattern_by_rule(rule)

    if pattern == PROVIDE_ACCESS:
        pass
    elif pattern == OTHER_PATTERN:
        # we only process a subset of patterns, and ignore the rest, they are not saved in the cache either (see contract.py#is_artifact_cacheable) and therefore requested from the connector everytime.
        # therefore ignore them in the validation
        pass
    elif pattern == PROHIBIT_ACCESS:
        raise RuleError('Access is prohibited')
    elif pattern == DURATION_USAGE:
        validate_rule_duration(rule, artifact)
    elif pattern == USAGE_DURING_INTERVAL or pattern == USAGE_UNTIL_DELETION:
        validate_rule_interval(rule)
    else:
        raise RuntimeError('An unexpected state has been reached')
    
    validate_rule_postduties(rule)

def validate_rule_duration(rule: Rule, artifact: Artifact):
    tdelta = get_duration(rule)
    start = artifact.creation_date.value

    deadline = start + tdelta

    if (datetime.now(deadline.tzinfo) > deadline):
        raise RuleError('Access duration is exceeded')

def validate_rule_interval(rule: Rule):
    start, end = get_interval(rule)

    if (datetime.now(end.tzinfo) > end or datetime.now(start.tzinfo) < start):
        raise RuleError('Access interval is either not entered yet, or is already over')

def validate_rule_postduties(rule: Rule):
    if not isinstance(rule, Permission):
        return
    
    for duty in rule.post_duty:
        # validate deletions
        validate_rule_post_duty_delete(duty)
                
def validate_rule_post_duty_delete(duty: Rule):
    for action in duty.action:
        if action.id == DELETE.id:
            deletion_date = get_date(duty)
            if datetime.now(deletion_date.tzinfo) > deletion_date:
                raise RuleError('Deletion date for the artifact has passed')

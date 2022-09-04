from datetime import datetime
from ..ids_information_model.contract import Contract
from ..ids_information_model.rule import Rule
from .rule import get_pattern_by_rule
from .pattern import *

def get_rules_from_contract(c: Contract) -> list[Rule]:
    return c.permission + c.obligation + c.prohibition

def is_artifact_cacheable(contract: Contract) -> bool:
    rules = get_rules_from_contract(contract)
    for rule in rules:
        pattern = get_pattern_by_rule(rule)
        if pattern == PROHIBIT_ACCESS or pattern == OTHER_PATTERN:
            return False

    return True

def select_contract_by_preferable_rules(contract_dicts: list[dict]):
    for c_dict in contract_dicts:
        if is_artifact_cacheable(Contract.parse_obj(c_dict)):
            return c_dict

    # no cacheable one found, return the first one
    return contract_dicts[0]

def is_contract_valid(contract: Contract) -> bool:
    display('checking contract validity', contract)

    # test contract duration
    present = datetime.now()
    if present > contract.contract_end or present < contract.contract_start
        return False

    return True
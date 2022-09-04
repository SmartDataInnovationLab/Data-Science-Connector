from ..ids_information_model.contract import Contract
from ..ids_information_model.artifact import Artifact
from .rule import get_pattern_by_rule
from .pattern import *
from .validation import is_contract_valid_for_artifact
from .contract_util import get_rules_from_contract

def is_artifact_cacheable(contract: Contract) -> bool:
    rules = get_rules_from_contract(contract)
    for rule in rules:
        pattern = get_pattern_by_rule(rule)
        if pattern == OTHER_PATTERN:
            return False

    return True

def select_valid_contract_by_preferable_rules(contract_dicts: list[dict], artifact: Artifact):
    valid_contracts = []
    for c_dict in contract_dicts:
        if is_contract_valid_for_artifact(Contract.parse_obj(c_dict), artifact):
            valid_contracts.append(c_dict)

    valid_and_cacheable_contracts = []
    for c_dict in valid_contracts:
        if is_artifact_cacheable(Contract.parse_obj(c_dict)):
            valid_and_cacheable_contracts.append(c_dict)

    if len(valid_and_cacheable_contracts) > 0:
        # there is at least one preferred contract, use it
        # use the last one (heuristic: later, newer, better)
        return valid_and_cacheable_contracts[len(valid_and_cacheable_contracts) - 1]

    if len(valid_contracts) > 0:
        # there is no cacheable contract, use at least valid one
        return valid_contracts[len(valid_contracts) - 1]

    # no valid contract
    return None

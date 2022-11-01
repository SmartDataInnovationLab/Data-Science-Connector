from ..ids_information_model.contract import Contract
from ..ids_information_model.rule import Rule

def get_rules_from_contract(c: Contract) -> list[Rule]:
    return c.permission + c.prohibition # + c.obligation
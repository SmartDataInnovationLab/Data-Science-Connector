from .action import Action
from .described import Described
from .constraint import Constraint

class Rule(Described):
    constraint: list[Constraint] = []
    action: list[Action] = []

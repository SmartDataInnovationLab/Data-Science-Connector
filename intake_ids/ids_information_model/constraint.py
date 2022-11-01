from typing import Any
from .ids_model import IDSModel
from .typed_literal import TypedLiteral
from .left_operand import LeftOperand
from .binary_operator import BinaryOperator

class Constraint(IDSModel):
    left_operand: LeftOperand
    operator: BinaryOperator
    # this is to broad and outside the scope imo, let's just take care of it when we need it
    right_operand: TypedLiteral[str] | str
    # truncated, there is more in the full model

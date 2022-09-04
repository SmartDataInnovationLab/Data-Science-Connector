from datetime import datetime
from .ids_model import IDSModel
from .permission import Permission
from .typed_literal import TypedLiteral
from .prohibition import Prohibition
from .duty import Duty

class Contract(IDSModel):
    contract_start: TypedLiteral[datetime] | None = None
    contract_end: TypedLiteral[datetime] | None = None
    contract_date: TypedLiteral[datetime] | None = None
    permission: list[Permission] = []
    prohibition: list[Prohibition] = []
    obligation: list[Duty] = []
    # truncated, there is more in the full model

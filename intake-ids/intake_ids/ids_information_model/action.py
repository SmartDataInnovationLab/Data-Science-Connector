from __future__ import annotations

from .ids_model import IDSModel
from .constraint import Constraint

class Action(IDSModel):
    pass
    # truncated, there is more in the full model

DELETE = Action.parse_obj({"@id": "idsc:DELETE"})
USE = Action.parse_obj({"@id": "idsc:USE"})

from __future__ import annotations

from .ids_model import IDSModel

class LeftOperand(IDSModel):
    pass
    # truncated, there is more in the full model

COUNT = LeftOperand.parse_obj({"@id": "idsc:COUNT"})
ELAPSED_TIME = LeftOperand.parse_obj({"@id": "idsc:ELAPSED_TIME"})
POLICY_EVALUATION_TIME = LeftOperand.parse_obj({"@id": "idsc:POLICY_EVALUATION_TIME"})
# truncated, there is more in the full model
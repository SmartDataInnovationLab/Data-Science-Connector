from __future__ import annotations

from .ids_model import IDSModel

class BinaryOperator(IDSModel):
    pass

AFTER = BinaryOperator.parse_obj({"@id": "idsc:AFTER"})
BEFORE = BinaryOperator.parse_obj({"@id": "idsc:BEFORE"})
SHORTER_EQ = BinaryOperator.parse_obj({"@id": "idsc:SHORTER_EQ"})
SHORTER = BinaryOperator.parse_obj({"@id": "idsc:SHORTER"})
LONGER_EQ = BinaryOperator.parse_obj({"@id": "idsc:LONGER_EQ"})
LONGER = BinaryOperator.parse_obj({"@id": "idsc:LONGER"})
TEMPORAL_EQUALS = BinaryOperator.parse_obj({"@id": "idsc:TEMPORAL_EQUALS"})
# there is more, but they are unnecessary
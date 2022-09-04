from __future__ import annotations

from .ids_model import IDSModel

class BinaryOperator(IDSModel):
    pass

AFTER = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/AFTER"})
BEFORE = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/BEFORE"})
SHORTER_EQ = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/SHORTER_EQ"})
SHORTER = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/SHORTER"})
LONGER_EQ = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/LONGER_EQ"})
LONGER = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/LONGER"})
TEMPORAL_EQUALS = BinaryOperator.parse_obj({"@id": "https://w3id.org/idsa/code/TEMPORAL_EQUALS"})
# there is more, but they are unnecessary
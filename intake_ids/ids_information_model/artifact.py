from datetime import datetime
from .ids_model import IDSModel
from .typed_literal import TypedLiteral

class Artifact(IDSModel):
    creation_date: TypedLiteral[datetime]
    byte_size: int
    check_sum: str

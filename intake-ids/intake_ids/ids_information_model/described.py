from .ids_model import IDSModel
from .typed_literal import TypedLiteral

class Described(IDSModel):
    title: list[TypedLiteral[str]] | None = None
    description: list[TypedLiteral[str]] | None = None
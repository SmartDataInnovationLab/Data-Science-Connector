from typing import Generic, TypeVar
from pydantic import Field
from pydantic.generics import GenericModel

TypeT = TypeVar('TypeT')

# This is a `lite` version, no need for details, we don't use them
class TypedLiteral(GenericModel, Generic[TypeT]):
    type: str = Field(..., alias='@type')
    value: TypeT = Field(..., alias='@value')
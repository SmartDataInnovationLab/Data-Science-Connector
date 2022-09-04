from pydantic import BaseModel, utils, Field
# Could use Owlready2, time

def to_ids(string: str) -> str:
    return 'ids:' + utils.to_lower_camel(string)

class IDSModel(BaseModel):
    id: str = Field(..., alias='@id')
    type: str | None = Field(None, alias='@type')

    class Config:
        alias_generator = to_ids
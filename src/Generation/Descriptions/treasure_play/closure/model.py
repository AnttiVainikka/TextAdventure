from pydantic import BaseModel, Field

class Model(BaseModel):
    closure: str = Field(title="The closure of the field")

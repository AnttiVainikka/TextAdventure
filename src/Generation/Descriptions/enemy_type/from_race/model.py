from pydantic import BaseModel, Field, conlist

class Model(BaseModel):
    Common: conlist(str, min_length=3) = Field(title=['', '', ''])
    Rare: conlist(str, min_length=3) = Field(title=['', '', ''])
    Epic: conlist(str, min_length=3) = Field(title=['', '', ''])
    Legendary: conlist(str, min_length=3) = Field(title=['', '', ''])

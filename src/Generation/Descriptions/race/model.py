from pydantic import BaseModel, conlist, Field

class Model(BaseModel):
    Friendly: conlist(str, min_length=3) = Field(title=['', '', ''])
    Neutral: conlist(str, min_length=3) = Field(title=['', '', ''])
    Aggressive: conlist(str, min_length=3) = Field(title=['', '', ''])

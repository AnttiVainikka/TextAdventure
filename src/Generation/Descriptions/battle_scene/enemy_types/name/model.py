from pydantic import BaseModel, Field, conlist

class Model(BaseModel):
    enemy_types: conlist(str) = Field(title='["", ..., ""]')

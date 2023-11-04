from pydantic import BaseModel, Field

class Model(BaseModel):
    names: list[str] = Field(title=['Name 1', 'Name 2', '...', 'Name N'])
from pydantic import BaseModel, Field

class Model(BaseModel):
    roles: list[str] = Field(title=['Role 1', 'Role 2', '...', 'Role N'])
from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title='Name of the equipment')
    description: str = Field(title='The description of the equipment')

from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title="The name of the skill")
    description: str = Field(title="The description of the skill")

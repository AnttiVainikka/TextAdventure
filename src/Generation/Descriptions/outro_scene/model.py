from pydantic import BaseModel, Field

class Model(BaseModel):
    context: str = Field(Title="The context the outro that can be printed to the player")
    
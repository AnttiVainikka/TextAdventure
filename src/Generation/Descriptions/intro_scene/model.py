from pydantic import BaseModel, Field

class Model(BaseModel):
    context: str = Field(Title="The context that can be printed to the player")
    
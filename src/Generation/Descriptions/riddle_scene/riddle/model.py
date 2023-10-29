from pydantic import BaseModel, Field

class Model(BaseModel):
    riddle: str = Field(title="The riddle printed to the player")
    answer: str = Field(title="The answer for the riddle")

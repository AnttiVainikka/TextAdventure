from pydantic import BaseModel, Field

class Model(BaseModel):
    boss_name: str = Field(title="The name of the boss")
    boss_description: str = Field(title="The description of the boss")
    boss_race: str = Field(title="The race of the boss")

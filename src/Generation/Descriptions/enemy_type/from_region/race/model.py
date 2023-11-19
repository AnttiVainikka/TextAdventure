from pydantic import BaseModel, Field

class Model(BaseModel):
    enemy_race: str = Field(title='The race of the enemy type')

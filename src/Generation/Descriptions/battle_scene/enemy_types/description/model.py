from pydantic import BaseModel, Field

class Model(BaseModel):
    enemy_type_description: str = Field(title='The description of the enemy type')

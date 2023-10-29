from pydantic import BaseModel, Field

class Model(BaseModel):
    mission: str = Field(title='The single, simple mission in the region')

from pydantic import BaseModel, Field

class Model(BaseModel):
    quest: str = Field(title='The quest in the region')

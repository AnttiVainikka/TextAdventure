from pydantic import BaseModel, Field

class Model(BaseModel):
    unique_name: str = Field(title='Unique name of the legendary leader')
    description: str = Field(title='Description of the legendary leader')

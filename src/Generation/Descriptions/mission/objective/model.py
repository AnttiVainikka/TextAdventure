from pydantic import BaseModel, Field

class Model(BaseModel):
    objective_entity: str = Field(title='The objective entity')

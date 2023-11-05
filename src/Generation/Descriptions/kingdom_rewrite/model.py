from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title='Name of the kingdom')
    geography: str = Field(title='Natural geography of the area')
    economy: str = Field(title='Overview on economy of the kingdom')

from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title='Name of the kingdom')
    geography: str = Field(title='Natural geography of the area')
    ruler_name: str = Field(title='Name of the King or Queen')
    economy: str = Field(title='Overview on economy of the kingdom')
    #calamity: str = Field(title='A calamity that has recently befell on the kingdom')
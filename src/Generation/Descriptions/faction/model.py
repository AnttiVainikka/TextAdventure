from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title='Name of the faction')
    overview: str = Field(title='A brief overview of the faction')
    motto: str = Field(title='Official motto of the faction')
    beliefs: str = Field(title='A summary of common beliefs of the faction')
    goals: str = Field(title='Overarching goals of the faction')
    needs: str = Field(title='What the faction needs/wants so much that they\'d join a rebellion for it?')
from pydantic import BaseModel, Field

class Model(BaseModel):
    name: str = Field(title='Name of the capital city')
    architecture: str = Field(title='How has the capital been built')
    population: str = Field(title='Roughly how big the city is')
    history: str = Field(title='A brief history of the capital city')
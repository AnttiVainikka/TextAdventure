from pydantic import BaseModel, Field


class Model(BaseModel):
    deeds: str = Field(title='An overview on what changes the ruler has brought to kingdom')
    personality: str = Field(title='A brief description of ruler\'s current personality')
    governance_style: str = Field(title='How does the ruler stay in power, despite being disliked')
    evil_deeds: str = Field(title='A brief overview what kind of actions make the ruler an evil tyrant')

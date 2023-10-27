from pydantic import BaseModel, Field


class Model(BaseModel):
    personality: str = Field(title='A brief description of ruler\'s personality')
    evil_deeds: str = Field(title='Questionable deeds that the ruler has done')
    governance_style: str = Field(title='How does the ruler stay in power, despite the dislike')
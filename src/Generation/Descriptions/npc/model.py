from pydantic import BaseModel, Field


class Model(BaseModel):
    personality: str = Field(title='A brief description of the character\'s personality')
    background: str = Field(title='Background story of the character')
    secrets: str = Field(title='Secrets that the character would want no one to know')

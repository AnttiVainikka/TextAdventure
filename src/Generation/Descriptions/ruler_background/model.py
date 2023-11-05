from pydantic import BaseModel, Field


class Model(BaseModel):
    personality: str = Field(title='What kind of person the current ruler used to be')
    origin: str = Field(title='A brief origin story of them')
    crisis: str = Field(title='A brief description of the crisis mentioned above - what enabled or forced them to go for throne?')
    rise_to_power: str = Field(title='How did the current ruler rise to power? What methods did they use?')
    motivation: str = Field(title='Why did they do it?')

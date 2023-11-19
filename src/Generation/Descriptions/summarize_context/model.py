from pydantic import BaseModel, Field

MAX_LENGTH = 50

class Model(BaseModel):
    summarized_context: str = Field(title=f'The summarized context at most {MAX_LENGTH} words')

from pydantic import BaseModel, Field

MAX_LENGTH = 300

class Model(BaseModel):
    summarized_context: str = Field(title=f'The summarized context at most {MAX_LENGTH} characters', max_length=MAX_LENGTH)

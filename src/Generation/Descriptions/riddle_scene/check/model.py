from pydantic import BaseModel, Field

class Model(BaseModel):
    is_it_correct: bool = Field(title="True if the answer was correct; False otherwise")

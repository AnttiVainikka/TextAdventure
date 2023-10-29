from pydantic import BaseModel, Field

class Model(BaseModel):
    context: str = Field(title="The context of the leaving of the chest")

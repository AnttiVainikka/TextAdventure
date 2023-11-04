from pydantic import BaseModel, Field, conlist

class Model(BaseModel):
    context: str = Field(title="The context of the field")
    look_around_choice: str = Field(title="The choice for look around")
    do_nothing_choice: str = Field(title="The choice for doing nothing")

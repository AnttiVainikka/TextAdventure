from pydantic import BaseModel, Field, conlist

class Model(BaseModel):
    looted_context: str = Field(title="The looted context of the place")
    look_around_choice: str = Field(title="The choice for look around again")
    do_nothing_choice: str = Field(title="The choice for do nothing")

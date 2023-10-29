from pydantic import BaseModel, conlist, Field

class Model(BaseModel):
    region_names: conlist(str, min_length=1) = Field(title='["", ..., ""]')

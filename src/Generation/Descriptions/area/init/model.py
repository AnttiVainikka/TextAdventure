from pydantic import BaseModel, Field, conlist

# It is necessary to the generate both the description and the name at the same time. Though it's probably not the nicest solution
class Model(BaseModel):
    areas: conlist(str) = Field(title=f'["area_name:area_description"]')

from pydantic import BaseModel, Field

class Model(BaseModel):
    region_description: str = Field(title="The description of the region.")

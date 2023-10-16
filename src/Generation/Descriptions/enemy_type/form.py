from pydantic import BaseModel, conlist

class form(BaseModel):
    Common: conlist(str, min_length=3) = ["", "", ""]
    Rare: conlist(str, min_length=3) = ["", "", ""]
    Epic: conlist(str, min_length=3) = ["", "", ""]
    Legendary: conlist(str, min_length=3) = ["", "", ""]

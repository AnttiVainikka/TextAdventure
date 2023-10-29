from dataclasses import dataclass, is_dataclass, fields
from typing import Type

def to_dict(obj: object) -> dict:
    if obj is None: return None
    if is_dataclass(obj): return to_dict_dataclass(obj)
    if isinstance(obj, list):
        return [to_dict(elem) for elem in obj]            
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        return obj

def to_dict_index(obj: object, l: list[object]) -> int | None:
    if obj is None or l is None: return None
    try:
        return l.index(obj)
    except ValueError:
        return None
    
def to_dict_dataclass(dc: object) -> dict:
    _fields = fields(type(dc))
    state = {}
    for field in _fields:
        state[f"{field.name}"] = to_dict(getattr(dc, field.name))
    return state
    
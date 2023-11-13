from Generation.generator import llm_create
from Characters.equipment import EquipmentRarity, EquipmentType

def generate(equipment_type: EquipmentType, rarity: EquipmentRarity, user_race: str, user_class: str, user_name: str = "") -> (str, str):
    data = llm_create("equipment", 1, equipment_type=equipment_type.name, user=_user_str(user_race, user_class, user_name), rarity=rarity.name)[0]
    return (data.name, data.description)

def _user_str(user_race: str, user_class: str, user_name: str) -> str:
    s = ""
    if not (user_name is None or user_name == ""):
        s += f"{user_name}, "
    s += f"a {user_race} {user_class}"
    return s

from enum import Enum
from Journey.utility import to_dict

class EquipmentType(Enum):
    Weapon = 1
    Armour = 2

class EquipmentRarity(Enum):
    Common = 1
    Rare = 2
    Epic = 3
    Legendary = 4

class Equipment():
    def __init__(self, type :EquipmentType = EquipmentType.Weapon,
                       rarity: EquipmentRarity = EquipmentRarity.Common,
                       stats :list = [0, 0],
                       name :str = "",
                       description :str = ""):
        """
        type: EquipmentType
        (more variety to armour pieces can be added later (gloves, boots...))
        stats: [physical damage/armour, magical damage/armour]
        description: for LLM to use when describing the equipment
        """
        self.type = type
        self.rarity = rarity
        self.name = name
        self.stats = stats
        self.description = description

    def __init_from_dict__(self, state: dict):
        self.type = EquipmentType(state["type"])
        self.rarity = EquipmentRarity(state["rarity"])
        self.name = state["name"]
        self.stats = state["stats"]
        self.description = state["description"]

    def create_from_dict(state: dict) -> "Equipment":
        equipment = Equipment.__new__(Equipment)
        equipment.__init_from_dict__
        return equipment

    def to_dict(self) -> dict:
        return {
            "type": to_dict(self.type.value),
            "rarity": to_dict(self.rarity.value),
            "name": to_dict(self.name),
            "stats": to_dict(self.stats),
            "description": to_dict(self.description)
        }

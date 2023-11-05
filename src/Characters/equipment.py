from enum import Enum

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

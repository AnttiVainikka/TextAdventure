from Characters.equipment import Equipment
from Characters.create import create_equipment

def print_equipment(equipment: Equipment):
    print(f"{equipment.type.name}: {equipment.name} ~ {equipment.rarity.name}")
    print(f"{equipment.description}")
    print(f"{equipment.stats}")

weapons_and_armours = []
weapons_and_armours.append(create_equipment("warrior", "Orc", "", 10, 1))
weapons_and_armours.append(create_equipment("mage", "Human", "", 10, 2))
weapons_and_armours.append(create_equipment("mage", "Troll", "", 10, 3))
weapons_and_armours.append(create_equipment("rogue", "Elf", "Lirelia Starwhisper", 10, 4))

for (weapon, armour) in weapons_and_armours:
    print_equipment(weapon)
    print("+++++")
    print_equipment(armour)
    print("-------------------------")

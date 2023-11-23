from Characters.equipment import Equipment, EquipmentRarity, EquipmentType
from Characters.character import Character
from ui.inventory_ui import print_inventory, view_item

test_common = Equipment(name="Wood club", stats=[3,0])
test_rare = Equipment(name="Fiery Waraxe"
                      , rarity = EquipmentRarity.Rare
                      , description="What happens when a description is too long?" + 
                      "This is What happens when a description is too long?" +
                      "This is What happens when a description is too long?" +
                      "This is What happens when a description is too long?")
test_epic = Equipment(name="Phalar Aluve", rarity = EquipmentRarity.Epic)
test_lege = Equipment(name="Frostmourne"
                      , rarity = EquipmentRarity.Legendary
                      , stats=[25,20]
                      , description="Bet you know what this is")
test_rare_armour = Equipment(name="Dark Justiciar Plate"
                        , rarity = EquipmentRarity.Rare
                        , type=EquipmentType.Armour,
                        stats=[15,2]
                        , description="A crude plate worn by Dark Justiciars, the elite of the goddess Shar.")
test_lege_armour = Equipment(name="Archmage robes"
                        , rarity = EquipmentRarity.Legendary
                        , type=EquipmentType.Armour,
                        stats=[5, 20]
                        , description="From some dunmer from Winterhold or smth.")
equipment_list = [test_common,
                  test_rare,
                  test_epic,
                  test_lege,
                  test_rare_armour,
                  test_lege_armour]

test_char = Character(kind="",
                      name="",
                      stats=[],
                      multipliers=[],
                      description="")
test_char.weapon = test_epic
test_char.armour = test_rare_armour
#print_inventory(equipment=equipment_list)
#view_item(character=test_char, equipment=test_lege)
view_item(character=test_char, equipment=test_lege_armour)
#print(Panel.fit("Hello, [red]World!"))
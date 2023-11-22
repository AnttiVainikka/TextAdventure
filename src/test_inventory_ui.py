from Characters.equipment import Equipment, EquipmentRarity, EquipmentType
from ui.inventory_ui import print_inventory

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
test_armour = Equipment(name="Dark Justiciar Plate"
                        , rarity = EquipmentRarity.Rare
                        , type=EquipmentType.Armour
                        , description="A crude plate worn by Dark Justiciars, the elite of the goddess Shar.")
equipment_list = [test_common,
                  test_rare,
                  test_epic,
                  test_lege,
                  test_armour]

print_inventory(equipment=equipment_list)
import sys
sys.path.append('../src/Characters')
from Characters.equipment import EquipmentRarity, EquipmentType
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from .battle_ui import clear_console

def construct_item_text(equipment):
  text = equipment.name
  if equipment.type == EquipmentType.Weapon:
    text += ('\n' + 'Type: Weapon' + 
             '\n' + 'Physical damage:' + str(equipment.stats[0]) + 
             '\n' + 'Magical damage:' + str(equipment.stats[1]))
  else: #equipment.type == EquipmentType.Armour
    text += ('\n' + 'Type: Armour' + 
             '\n' + 'Physical protection:' + str(equipment.stats[0]) + 
             '\n' + 'Magical protection:' + str(equipment.stats[1]))
  text += '\n' + 'Description:' + equipment.description
  return text


def construct_item_panel(index: int, equipment_list: list): #Forms a tile to display an item
  if (index >= len(equipment_list)): #In case that there is no more equipment to show
    return Panel("", style = "bright_black")
  else :
    equipment = equipment_list[index]
    text = construct_item_text(equipment=equipment)
    if equipment.rarity == EquipmentRarity.Common:
      return Panel(text)
    if equipment.rarity == EquipmentRarity.Rare:
      return Panel(text, style = "bright_cyan")
    if equipment.rarity == EquipmentRarity.Epic:
      return Panel(text, style = "bright_magenta")
    if equipment.rarity == EquipmentRarity.Legendary:
      return Panel(text, style = "bright_yellow")

def construct_inventory_row(index: int, equipment_list: list): #Forms one row of 3 items
  layout = Layout()
  layout.split_row(
    construct_item_panel(index, equipment_list),
    construct_item_panel(index+1, equipment_list),
    construct_item_panel(index+2, equipment_list)
    #There is probably a better way to assign the "indexes" 
    #for the slots but this way is simple and works 
  )
  return layout

def construct_inventory_grid(equipment: list): #Forms a 3x3 grid, so the inventory doesn't show more than 9 items
  layout = Layout()
  layout.split_column(
    Layout(Panel("",style="black"),name="top_buffer", size = 2),
    construct_inventory_row(index=0, equipment_list=equipment),
    construct_inventory_row(index=3, equipment_list=equipment),
    construct_inventory_row(index=6, equipment_list=equipment)
  ) 
  #Same thing here as on lines 44-45
  return(layout)

def print_inventory(equipment :list):
  clear_console()

  print(construct_inventory_grid(equipment))

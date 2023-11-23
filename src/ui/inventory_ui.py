import sys
sys.path.append('../src/Characters')
from Characters.equipment import EquipmentRarity, EquipmentType
from rich import print
from rich.layout import Layout
from rich.panel import Panel
from .battle_ui import clear_console

def form_equipment_comparation_text(character, new_equipment):
  current_equipment_text = ''
  new_equipment_text = ''

  if new_equipment.type == EquipmentType.Weapon:

    current_equipment = character.weapon
    new_has_better_physical = new_equipment.stats[0] > current_equipment.stats[0]
    new_has_better_magical = new_equipment.stats[1] > current_equipment.stats[1]
    current_has_better_physical = current_equipment.stats[0] > new_equipment.stats[0]
    current_has_better_magical = current_equipment.stats[1] > new_equipment.stats[1]

    current_equipment_text += ('Current weapon: ' + current_equipment.name + '\n')
    new_equipment_text += ('New weapon: ' + new_equipment.name + '\n')

    if (current_has_better_physical):
      current_equipment_text += ('Physical damage: ' + '[green]' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical damage: ' + '[red]' + str(new_equipment.stats[0]) + '\n')
    elif (new_has_better_physical):
      current_equipment_text += ('Physical damage: ' + '[red]' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical damage: ' + '[green]' + str(new_equipment.stats[0]) + '\n')
    else: #The equipment have equal physical damage
      current_equipment_text += ('Physical damage: ' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical damage: ' + str(new_equipment.stats[0]) + '\n')

    if (current_has_better_magical):
      current_equipment_text += ('[white]Magical damage: ' + '[green]' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical damage: ' + '[red]' + str(new_equipment.stats[1]) + '\n')
    elif (new_has_better_magical):
      current_equipment_text += ('[white]Magical damage: ' + '[red]' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical damage: ' + '[green]' + str(new_equipment.stats[1]) + '\n')
    else: #The equipment have equal magical damage
      current_equipment_text += ('[white]Magical damage: ' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical damage: ' + str(new_equipment.stats[1]) + '\n')

    current_equipment_text += ('[white]Description: ' + current_equipment.description)
    new_equipment_text += ('[white]Description: ' + new_equipment.description)
    
  else: #new_equipment.type == EquipmentType.Armour
    current_equipment = character.armour
    new_has_better_physical = new_equipment.stats[0] > current_equipment.stats[0]
    new_has_better_magical = new_equipment.stats[1] > current_equipment.stats[1]
    current_has_better_physical = current_equipment.stats[0] > new_equipment.stats[0]
    current_has_better_magical = current_equipment.stats[1] > new_equipment.stats[1]

    current_equipment_text += ('Current armour: ' + current_equipment.name + '\n')
    new_equipment_text += ('New armour: ' + new_equipment.name + '\n')

    if (current_has_better_physical):
      current_equipment_text += ('Physical protection: ' + '[green]' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical protection: ' + '[red]' + str(new_equipment.stats[0]) + '\n')
    elif (new_has_better_physical):
      current_equipment_text += ('Physical protection: ' + '[red]' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical protection: ' + '[green]' + str(new_equipment.stats[0]) + '\n')
    else: #The equipment have equal physical protection
      current_equipment_text += ('Physical protection: ' + str(current_equipment.stats[0]) + '\n')
      new_equipment_text += ('Physical protection: ' + str(new_equipment.stats[0]) + '\n')

    if (current_has_better_magical):
      current_equipment_text += ('[white]Magical protection: ' + '[green]' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical protection: ' + '[red]' + str(new_equipment.stats[1]) + '\n')
    elif (new_has_better_magical):
      current_equipment_text += ('[white]Magical protection: ' + '[red]' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical protection: ' + '[green]' + str(new_equipment.stats[1]) + '\n')
    else: #The equipment have equal magical protection
      current_equipment_text += ('[white]Magical protection: ' + str(current_equipment.stats[1]) + '\n')
      new_equipment_text += ('[white]Magical protection: ' + str(new_equipment.stats[1]) + '\n')

    current_equipment_text += ('[white]Description: ' + current_equipment.description)
    new_equipment_text += ('[white]Description: ' + new_equipment.description)
        


  texts = [current_equipment_text, new_equipment_text]
  return texts

def view_item(equipment, character):
  texts = form_equipment_comparation_text(character=character,
                                          new_equipment=equipment)
  current_equipment_text = texts[0]
  new_equipment_text = texts[1]

  layout = Layout()
  layout.split_column(
    Layout(Panel("",style="black"),size=2),
    Layout(name="equipment", size=25))
  layout["equipment"].split_row(
    Panel(current_equipment_text),
    Panel(new_equipment_text)
  )
  clear_console()
  print(layout)



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

from rich import print
from rich.layout import Layout
from rich.panel import Panel

def construct_skill_panel(skill):
  panel = Panel()



def construct_skills_layout(skills: list):
  layout = Layout()

  if len(skills) == 0:
    layout.split_row(Panel("This character doesn't have any skills. :("))
  elif  len(skills) == 1:
    layout.split_row(
      Panel()
      )

  return layout

def view_character(character):

  layout = Layout()
  hp = character.stats["hp"]
  weapon = character.weapon
  armour = character.armour
  layout.split_column(
    Layout(Panel(character.name + "\nLvl:" + str(character.level) + "Class:" + character.type)),
    Layout(Panel(character.description)),
    Layout(Panel("HP:" + str(hp) + "/" + str(hp+character.lost_hp))),
    Layout(Panel("Atk:" + str(character.stats[1]))),
    Layout(Panel("Magic:" + str(character.stats[2]))),
    Layout(Panel("\nWeapon\n\n" + weapon.name + "\nAttack:" + weapon.stats[0] +  "Magic:" + weapon.stats[1] + "\n" + weapon.description)),
    Layout(Panel("\nArmour\n\n" + armour.name + "\nDefense:" + armour.stats[0] + "Magic Defense:" + armour.stats[1] + "\n" + armour.description)),
    Layout(Panel("\nArmour\n\n" + armour.name + "\nDefense:" + armour.stats[0] + "Magic Defense:" + armour.stats[1] + "\n" + armour.description))
    
  )
  print(layout)
  #\nArmour\n\n{armour.name}\nDefense: {armour.stats[0]}  Magic Defense: {armour.stats[1]}\n{armour.description}

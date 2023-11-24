from rich import print
from rich.layout import Layout
from rich.panel import Panel

def construct_skill_panel(skill):
  text = skill.name + " " + str(skill.uses_remaining) + "/" + str(skill.uses) + "\n\n" + skill.description +"\n"
  if skill.aoe:
    aoe = "all targets"
  else:
    aoe = "Single target"
  
  if skill.multiplier < 0:
    text += ("\nHeals " + aoe + " with multiplier " + str(-skill.multiplier) + ". Uses" + skill.stat)
  else:
    text += ("\nDeals damage to " + aoe + " with multiplier " + str(skill.multiplier) + ". Uses " + skill.stat)
  panel = Panel(text)
  return panel



def construct_skills_layout(skills: list):
  layout = Layout()

  if len(skills) == 0:
    layout.split_row(Panel("This character doesn't have any skills. :("))
  elif  len(skills) == 1:
    layout.split_row(
      construct_skill_panel(skills[0])
      )
  elif  len(skills) == 2:
    layout.split_row(
      construct_skill_panel(skills[0]),
      construct_skill_panel(skills[1])
      )
  elif  len(skills) == 3:
    layout.split_row(
      construct_skill_panel(skills[0]),
      construct_skill_panel(skills[1]),
      construct_skill_panel(skills[2])
      )
  elif  len(skills) == 4:
    upper_layout = Layout()
    upper_layout.split_row(
      construct_skill_panel(skills[0]),
      construct_skill_panel(skills[1]),
      construct_skill_panel(skills[2])
    )
    lower_layout = Layout()
    lower_layout.split_row(
      construct_skill_panel(skills[3])
    )
    layout.split_column(
      upper_layout,
      lower_layout
    )
  elif  len(skills) == 5:
    upper_layout = Layout()
    upper_layout.split_row(
      construct_skill_panel(skills[0]),
      construct_skill_panel(skills[1]),
      construct_skill_panel(skills[2])
    )
    lower_layout = Layout()
    lower_layout.split_row(
      construct_skill_panel(skills[3]),
      construct_skill_panel(skills[4])
    )
    layout.split_column(
      upper_layout,
      lower_layout
    )
  else:
    upper_layout = Layout()
    upper_layout.split_row(
      construct_skill_panel(skills[0]),
      construct_skill_panel(skills[1]),
      construct_skill_panel(skills[2])
    )
    lower_layout = Layout()
    lower_layout.split_row(
      construct_skill_panel(skills[3]),
      construct_skill_panel(skills[4]),
      construct_skill_panel(skills[5])
    )
    layout.split_column(
      upper_layout,
      lower_layout
    )
  return layout

def print_character_view(character):

  layout = Layout()
  hp = character.stats["hp"]
  weapon = character.weapon
  armour = character.armour
  stats_and_desc_layout = Layout()
  stats_layout = Layout(Panel(character.name + "\nLvl: " + str(character.level) + " \n\nClass: " + character.type +
           "\nHP:" + str(hp) + "/" + str(hp+character.lost_hp) + 
           " \nAtk:" + str(character.stats["atk"]) +
           " \nMagic:" + str(character.stats["magic"])))
  desc_layout = Layout(Panel(character.description))
  stats_layout.ratio=1
  desc_layout.ratio=3
  stats_and_desc_layout.split_row(
    stats_layout,
    desc_layout
  )
  stats_and_desc_layout.size=10
  stats_and_desc_layout.ratio
  equipment_layout = Layout()
  equipment_layout.split_row(
    Panel("\nWeapon\n\n" + weapon.name + "\nAttack: " + str(weapon.stats[0]) +  " Magic: " + str(weapon.stats[1]) + "\n\n" + weapon.description),
    Panel("\nArmour\n\n" + armour.name + "\nDefense: " + str(armour.stats[0]) + " Magic Defense: " + str(armour.stats[1]) + "\n\n" + armour.description)
    )
  equipment_layout.size=12
  layout.split_column(
    Layout(Panel("",style="black"),size=2),
    stats_and_desc_layout,
    equipment_layout,
    Layout(construct_skills_layout(character.skills))

   
                     
  )
  print(layout)

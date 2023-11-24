import os
from rich import print
from rich.layout import Layout
from rich.panel import Panel

def construct_character_panel(fighter, relation: str):
  if (relation == "enemies"):
     return Panel("[red]" + fighter.name + '\n' +
                '[white]HP:'+ str(fighter.stats["hp"]) +'/' + str(fighter.stats["hp"]+fighter.lost_hp) + '\n' + 
                'lvl:'+ str(fighter.level))
  else: #relation == allies
    return Panel("[green]" + fighter.name + '\n' +
                '[white]HP:'+ str(fighter.stats["hp"]) +'/' + str(fighter.stats["hp"]+fighter.lost_hp) + '\n' + 
                'lvl:'+ str(fighter.level))

def construct_character_row(fighters: [], layout: Layout,relation: str):
    #TERRIBLE solution but no alternative was found :/
    if (len(fighters)==1):
      layout[relation].split_row(
        construct_character_panel(fighters[0], relation)
      )
    elif (len(fighters)==2):
      layout[relation].split_row(
        construct_character_panel(fighters[0], relation),
        construct_character_panel(fighters[1], relation)
      )
    elif (len(fighters)==3):
      layout[relation].split_row(
        construct_character_panel(fighters[0], relation),
        construct_character_panel(fighters[1], relation),
        construct_character_panel(fighters[2], relation)
      )
    elif (len(fighters)==4):
      layout[relation].split_row(
        construct_character_panel(fighters[0], relation),
        construct_character_panel(fighters[1], relation),
        construct_character_panel(fighters[2], relation),
        construct_character_panel(fighters[3], relation)
      ), relation
    else : 
      #Max number of fighters per side at a 
      # single point in time is 5, can be changed
      layout[relation].split_row(
        construct_character_panel(fighters[0], relation),
        construct_character_panel(fighters[1], relation),
        construct_character_panel(fighters[2], relation),
        construct_character_panel(fighters[3], relation),
        construct_character_panel(fighters[4], relation)
      )

def clear_console():
  if(os.name == 'posix'):
    os.system('clear')
  else:
   os.system('cls')

def print_battle_status(enemies :list, friends :list, current_player,target):
    layout = Layout()
    counter = 0
    if not target:
      layout.split_column(
        Layout(Panel("",style="black"),name="top_buffer",size=2),
        Layout(name="enemies", size=10),
        Layout(Panel("",style="black"),name="top_buffer",size=5),
        Layout(name="allies", size=10),
        Layout(Panel("[white]1:  Attack\n2:  Skill\n3:  Run\n4:  View\n", style="black"), size=6)
      )
    elif target == "all":
      counter = 1
      text = "[white]\n"
      for p in friends:
          text += f"{counter}:   {p.name} HP:{p.stats['hp']}/{p.stats['hp']+p.lost_hp} \n" 
          counter += 1
      for e in enemies:
          text += f"{counter}:   {e.name} HP:{e.stats['hp']}/{e.stats['hp']+e.lost_hp} \n"
          counter += 1
      text += f"\n{counter}:  Back"
      layout.split_column(
        Layout(Panel("",style="black"),name="top_buffer",size=2),
        Layout(name="enemies", size=10),
        Layout(Panel("",style="black"),name="top_buffer",size=5),
        Layout(name="allies", size=10),
        Layout(Panel(text, style="black"), size=14)
      )
    elif target == "players":
      counter = 1
      text = "[white]\n"
      for p in friends:
          text += f"{counter}:   {p.name} HP:{p.stats['hp']}/{p.stats['hp']+p.lost_hp} \n" 
          counter += 1
      text += f"\n{counter}:  Back"
      layout.split_column(
        Layout(Panel("",style="black"),name="top_buffer",size=2),
        Layout(name="enemies", size=10),
        Layout(Panel("",style="black"),name="top_buffer",size=5),
        Layout(name="allies", size=10),
        Layout(Panel(text, style="black"), size=14)
      )
    elif target == "enemies":
      counter = 1
      text = "[white]\n"
      for e in enemies:
          text += f"{counter}:   {e.name} HP:{e.stats['hp']}/{e.stats['hp']+e.lost_hp} \n"
          counter += 1
      text += f"\n{counter}:  Back"
      layout.split_column(
        Layout(Panel("",style="black"),name="top_buffer",size=2),
        Layout(name="enemies", size=10),
        Layout(Panel("",style="black"),name="top_buffer",size=5),
        Layout(name="allies", size=10),
        Layout(Panel(text, style="black"), size=14)
      )
    elif target == "skills":
        counter = 1
        text = "[white]\n"
        skills = current_player.skills
        for s in skills:
            text += f"{counter}:   {s.name}  {s.uses_remaining}/{s.uses} \n" 
            counter += 1
        text += f"\n{counter}:  Back"
        layout.split_column(
          Layout(Panel("",style="black"),name="top_buffer",size=2),
          Layout(name="enemies", size=10),
          Layout(Panel("",style="black"),name="top_buffer",size=5),
          Layout(name="allies", size=10),
          Layout(Panel(text, style="black"), size=14)
        )
    construct_character_row(fighters=enemies, layout=layout, relation="enemies")
    construct_character_row(fighters=friends, layout=layout, relation="allies")
    print(layout)
    return counter

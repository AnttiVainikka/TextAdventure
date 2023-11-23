import os
from rich import print
from rich.layout import Layout
from rich.panel import Panel

def construct_character_panel(fighter):
  return Panel(fighter.name + '\n' +
                'HP:'+ str(fighter.stats["hp"]-fighter.lost_hp) +'/' + str(fighter.stats["hp"]) + '\n' + 
                'lvl:'+ str(fighter.level))

def construct_character_row(fighters: [], layout: Layout,relation: str):
    #TERRIBLE solution but no alternative was found :/
    if (len(fighters)==1):
      layout[relation].split_row(
        construct_character_panel(fighters[0])
      )
    elif (len(fighters)==2):
      layout[relation].split_row(
        construct_character_panel(fighters[0]),
        construct_character_panel(fighters[1])
      )
    elif (len(fighters)==3):
      layout[relation].split_row(
        construct_character_panel(fighters[0]),
        construct_character_panel(fighters[1]),
        construct_character_panel(fighters[2])
      )
    else : 
      #Max number of fighters per side at a 
      # single point in time is 4, can be changed
      layout[relation].split_row(
        construct_character_panel(fighters[0]),
        construct_character_panel(fighters[1]),
        construct_character_panel(fighters[2]),
        construct_character_panel(fighters[3])
      )

def clear_console():
  if(os.name == 'posix'):
    os.system('clear')
  else:
   os.system('cls')

def print_battle_status(enemies :list, friends :list):
    layout = Layout()
    layout.split_column(
      Layout(Panel("",style="black"),name="top_buffer",size=2),
      Layout(name="enemies", size=10),
      Layout(Panel("",style="black"),name="top_buffer",size=5),
      Layout(name="allies", size=10)
    )
    construct_character_row(fighters=enemies, layout=layout, relation="enemies")
    construct_character_row(fighters=friends, layout=layout, relation="allies")
    clear_console()
    print(layout)

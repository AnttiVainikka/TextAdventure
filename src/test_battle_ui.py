from Characters.character import Character
from ui.battle_ui import print_battle_status

defaultstats = {}
defaultstats["hp"] = 30
fren1 = Character(kind="half-elf",
                        name="Astarion",
                        stats=defaultstats,
                        multipliers=0,
                        description="vambyr :D")
fren2 = Character(kind="dog",
                        name="Scratch",
                        stats=defaultstats,
                        multipliers=0,
                        description="best boi")

enem1 = Character(kind="Drow",
                        name="Minthara",
                        stats=defaultstats,
                        multipliers=0,
                        description="")
enem2 = Character(kind="Orc",
                        name="Grommash",
                        stats=defaultstats,
                        multipliers=0,
                        description="")
enem3 = Character(kind="Human",
                        name="Lord Enver Gortash",
                        stats=defaultstats,
                        multipliers=0,
                        description="")

enem2.lost_hp += 5

ally_list = [fren1, fren2]
enemy_list = [enem1, enem2, enem3]
print_battle_status(enemies=enemy_list, friends=ally_list)
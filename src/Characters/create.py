from Characters.character import Character
from Characters.equipment import Equipment
from Characters.skill import Skill

def create_main_character():
    """ Creating the preset character that can be used before
    we enable the player to create their own character """
    name = "Hero"
    level = 1
    description = "Preset main character"
    stats = {}
    #starting stats and multiplier for stat growth per level up
    hp = [30,1.5]
    atk = [10,1.5]
    magic = [10,1.5]
    stats["hp"] = []
    stats["atk"] = []
    stats["magic"] = []
    for i in range(1,11):
        stats["hp"].append(hp[0])
        stats["atk"].append(atk[0])
        stats["magic"].append(magic[0])
        hp[0] *= hp[1]
        atk[0] *= atk[1]
        magic[0] *= magic[1]
    main_character = Character(name,stats,level,description)
    sword = Equipment("weapon",[12,0],"Basic iron sword")
    main_character.weapon = sword
    fireball = Skill("Fire Ball",1.5,"magic",5,"Hurl a ball of fire at your enemy")
    heal = Skill("Lesser Heal", -0.8,"magic",8,"Use magic to mend wounds")
    main_character.skills.append(fireball)
    main_character.skills.append(heal)
    armour = Equipment("armour",[5,5],"Hero's armour")
    main_character.armour = armour
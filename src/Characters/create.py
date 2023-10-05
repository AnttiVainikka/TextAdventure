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
    stats["hp"] = 30
    stats["atk"] = 10
    stats["magic"] = 10
    multipliers = {}
    multipliers["hp"] = 1.5
    multipliers["atk"] = 1.5
    multipliers["magic"] = 1.5
    main_character = Character(name,stats,level,description)
    main_character.multipliers = multipliers
    sword = Equipment("weapon",[12,0],"Basic iron sword")
    main_character.weapon = sword
    fireball = Skill("Fire Ball",1.5,"magic",5,"Hurl a ball of fire at your enemy",False,False)
    heal = Skill("Lesser Heal", -0.8,"magic",8,"Use magic to mend wounds",True,False)
    shockwave = Skill("Shockwave", 500, "atk", 100, "Use to defeat everything",False,True)
    main_character.skills.extend([fireball,heal,shockwave])
    armour = Equipment("armour",[5,5],"Hero's armour")
    main_character.armour = armour
    return main_character

def create_goblins():
    """ Creating 4 goblins to test fighting against """
    level = 1
    description = "Weak looking Goblin"
    goblin1 = Character("Goblin Warrior",{},level,description)
    goblin2 = Character("Goblin Mage",{},level,description)
    goblin3 = Character("Goblin Ranger",{},level,description)
    goblin4 = Character("Goblin Hunter",{},level,description)
    goblins = [goblin1,goblin2,goblin3,goblin4]
    for goblin in goblins:
        stats = {}
        stats["hp"] = 30
        stats["atk"] = 1
        stats["magic"] = 1
        goblin.stats = stats
        goblin.given_exp = 100
    return goblins

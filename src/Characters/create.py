from Characters.character import Character
from Characters.equipment import Equipment
from Characters.skill import Skill
from Characters.skill import SkillRarity
from Generation.skill import generate as generate_skill
from random import randint

def create_main_character():
    """ Creating the preset character that can be used before
    we enable the player to create their own character """
    name = "Hero"
    description = "Preset main character"
    stats = {}
    stats["hp"] = 30
    stats["atk"] = 10
    stats["magic"] = 10
    multipliers = {}
    multipliers["hp"] = 1.05
    multipliers["atk"] = 1.05
    multipliers["magic"] = 1.05
    main_character = Character(name,stats,multipliers,description)
    sword = Equipment("weapon",[12,0],"Basic iron sword")
    main_character.weapon = sword
    fireball = Skill("Fire Ball",1.5,"magic",5,"Hurl a ball of fire at your enemy",False,False)
    heal = Skill("Lesser Heal", -0.8,"magic",8,"Use magic to mend wounds",True,False)
    shockwave = Skill("Shockwave", 500, "atk", 100, "Use to defeat everything",False,True)
    main_character.skills.extend([fireball,heal,shockwave])
    armour = Equipment("armour",[5,5],"Hero's armour")
    main_character.armour = armour
    main_character.gain_exp(100)
    return main_character

def create_enemies(level: int, difficulty: int):
    """ Returns a list of characters that can be used to battle against
    level: average level of enemies
    difficulty: 1-8, how many enemies and of what rarity """
    try:
        if difficulty > 8:
            difficulty = 8
        if difficulty < 1:
            difficulty = 1
    except TypeError:
        difficulty = 3
    enemies = []
    #TODO use LLM to generate race which will be used for each enemy generated
    while difficulty > 0:
        max_rarity = min([4,difficulty])
        rarity = randint(1,max_rarity)
        if len(enemies) == 4:
            rarity = max_rarity
            difficulty -= difficulty
        lvl = max([1,level-7+rarity*3])
        type = ["warrior","rogue","mage"][randint(0,2)]
        name = f'{["Beginner","Advanced","Expert","Legendary"][rarity-1]} {type}'
        description = "todo"
        #TODO Generate name and description for enemy with LLM using type, race, rarity...
        enemy = create_character(name,description,type,lvl,rarity)
        enemies.append(enemy)
        difficulty -= rarity
    return enemies

def create_character(name :str, description: str, type :str, level: int, rarity: int):
    """ Generates a character of given type and level
    name: name for the character
    description: short description for llm purposes
    type: warrior, rogue or mage, anything else defaults to mage
    level: the higher the stronger, currently capped at 100
    rarity: common, rare, epic, legendary represented by 1,2,3,4 respectively
    """
    #TODO if we want to create more types for characters, it could be good to make a class for types and have its
    # parameters include the necessary stats to prevent the need for long if -> elif patches of code.
    scaling = [0,1.01,1.025,1.04,1.06] # 1.01 for common enemies, 1.025 for rare and so on
    stats = {}

    #Randomly generate a starting value for each stat based on type
    if type == "warrior": # HP > atk > magic
        stats["hp"] = randint(35,40)
        stats["atk"] = randint(8,10)
        stats["magic"] = randint(1,3)
    elif type == "rogue": # atk > HP = magic
        stats["hp"] = randint(24,30)
        stats["atk"] = randint(12,15)
        stats["magic"] = randint(5,8)
    else: #mage   magic >> atk = HP
        stats["hp"] = randint(18,24)
        stats["atk"] = randint(2,5)
        stats["magic"] = randint(13,18)

    #Assign multipliers based on scaling
    multipliers = {}
    multipliers["hp"] = scaling[rarity]
    multipliers["atk"] = scaling[rarity]
    multipliers["magic"] = scaling[rarity]

    #Create character, level them up and give them equipment
    kind = "?" #what does kind mean/do?
    character = Character(kind,name,stats,multipliers,description)
    character.given_exp = level * 5
    for exp in range (1,level):
        character.gain_exp(exp*10)
    equipment = create_equipment(description,type,level,rarity)
    character.weapon = equipment[0]
    character.armour = equipment[1]

    #Give character skills. One when hitting level 20 and extra skills based on rarity
    if level >= 20:
        character.skills.append(create_skill(type,rarity))
    if rarity > 1:
        character.skills.append(create_skill(type,rarity-1))
    if rarity > 2:
        character.skills.append(create_skill(type,rarity-2))
    if rarity == 4:
        character.skills.append(create_skill(type,rarity-1))
    return character

def create_equipment(description :str, type: str, level: int, rarity: int):
    """ Takes description, type, level and rarity of the character the equipment is created for
    as parameters and returns a list of [weapon,armour] """
    weapon_desc = "todo"
    armour_desc = "todo"
    # TODO generate the description for the equipment with LLM, give description, type, level and rarity of character as context
    damage = [2.0, 2.5, 3.0, 3.5, 4.0][randint(0,4)] * 0.2 * rarity * level
    defense = [2.0, 2.5, 3.0, 3.5, 4.0][randint(0,4)] * 0.2 * rarity * level
    if type == "warrior":
        wstats = [int(damage*randint(8,12)*0.1),int(damage*randint(6,10)*0.1)]
        astats = [int(defense*randint(8,12)*0.1),int(defense*randint(12,15)*0.1)]
    elif type == "rogue":
        wstats = [int(damage*randint(10,14)*0.1),int(damage*randint(12,15)*0.1)]
        astats = [int(defense*randint(10,14)*0.1),int(defense*randint(6,10)*0.1)]
    else: #mage
        wstats = [damage*randint(1,12)*0.1,damage*randint(14,18)*0.1]
        astats = [defense*randint(1,12)*0.1,defense*randint(4,8)*0.1]
    weapon = Equipment("weapon",wstats,weapon_desc)
    armour = Equipment("armour",astats,armour_desc)
    return [weapon,armour]

def create_skill(type: str, rarity: int):
    """
    type: warrior/rogue/mage
    rarity: common, rare, epic, legendary represented by 1,2,3,4 respectively

    Returns: Skill object 
    """
    # Makes the skill hit every target with 1 in 4 chance
    if randint(1,4) == 1:
        aoe = True
    else:
        aoe = False

    # Makes the skill heal allies with 1 in 4 chance, not allowed for rogues
    if type != "rogue":
        if randint(1,4) == 1:
            ally = True
        else:
            ally = False
    else:
        ally = False

    # Randomly determines if skill uses atk or magic. Chance depends on class.
    if type == "warrior":
        if randint(1,5) == 1:
            stat = "magic"
        else:
            stat = "atk"
    elif type == "rogue":
        if randint(1,3) == 1:
            stat = "magic"
        else:
            stat = "atk"
    else: #mage
        if randint(1,8) == 1:
            stat = "atk"
        else:
            stat = "magic"

    multiplier = 0.1 * [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0][randint(0,6)] * rarity + 1
    if ally:
        multiplier *= -0.5
    if aoe:
        multiplier *= 0.5
    uses = randint(5,10)-rarity
    if aoe:
        aoe_desc="All"
    else:
        aoe_desc="Single"
    name = f"{stat} {round(multiplier,1)} {aoe_desc}"
    description = "todo"
    # TODO generate name and description based on type, rarity, stat, aoe and ally

    return Skill(name,multiplier,stat,uses,description,ally,aoe)


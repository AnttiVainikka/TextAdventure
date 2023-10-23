from time import sleep
from random import randint
class Character():
    def __init__(self, kind :str, name :str, stats :dict, multipliers :int, description :str):
        """ Used for both playable and npc characters. """
        self.kind = kind
        self.name = name
        self.stats = stats
        self.multipliers = multipliers
        self.level = 1
        self.exp = 0
        self.skills = []
        self.weapon = Equipment("weapon",[0,0],"Has to have some weapon to avoid errors")
        self.armour = Equipment("armour",[0,0],"Has to have some armour to avoid errors")
        self.description = description
        self.alive = True
        self.lost_hp = 0
        self.given_exp = 0 # how much exp enemy gives when defeated
        self.enemy = False #change to True if npc turns hostile to player
        # self.skillset could be implemented to have character learn specific skills
        # at specific levels
    
    def gain_exp(self,exp):
        """ Each level up takes current level * 10 experience. """
        self.exp += exp
        while True:
            if self.exp >= self.level * 10 and self.level <= 100:
                self.exp -= self.level * 10
                self.level += 1
                self.stats["hp"] += self.lost_hp
                self.lost_hp = 0
                self.stats["hp"] = max([int(self.multipliers["hp"] * self.stats["hp"]),self.stats["hp"]+1])
                self.stats["atk"] = max([int(self.multipliers["atk"] * self.stats["atk"]),self.stats["atk"]+1])
                self.stats["magic"] = max([int(self.multipliers["magic"] * self.stats["magic"]),self.stats["magic"]+1])
            else:
                break

    def take_damage(self,damage):
        """ Use this to damage or heal characters. Healing done
        with negative numbers. Returns "dead" if damage is fatal.
        Otherwise returns damage taken """
        if damage < 0:
            if self.lost_hp + damage <= 0:
                self.stats["hp"] += self.lost_hp
                self.lost_hp = 0
            else:
                self.stats["hp"] -= damage
                self.lost_hp += damage
            return True

        if self.stats["hp"] - damage <= 0:
            self.lost_hp += self.stats["hp"]
            self.stats["hp"] = 0
            self.alive = False
            return "dead" 
        else:
            self.stats["hp"] -= damage
            self.lost_hp += damage
        return True

class Equipment():
    def __init__(self, type :str, stats :list, description :str):
        """
        type: weapon/armour
        (more variety to armour pieces can be added later (gloves, boots...))
        stats: [physical damage/armour, magical damage/armour]
        description: for LLM to use when describing the equipment
        """
        self.type = type
        self.stats = stats
        self.description = description
        self.durability = 100 # Do we want them to break eventually?

class Skill():
    def __init__(self, name :str, multiplier :float, stat :str, uses :int, description :str, ally: bool, aoe: bool):
        """
        name: name of the skill
        multiplier: damage of skill = (character_stat + weapon_stat) * multiplier
        stat: which stat is used for damage calculation (atk,magic)
        uses: how many times skill can be used
        description: how the LLM will describe it when asked
        ally: is the skill cast on allies (True) or enemies (False)
        aoe: does the skill affect all allies/enemies
        """
        self.name = name
        self.multiplier = multiplier
        self.stat = stat
        self.uses = uses
        self.uses_remaining = uses
        self.description = description
        self.ally = ally
        self.aoe = aoe
    def restore_uses(self):
        self.uses_remaining = self.uses

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
        name = f"{["Beginner","Advanced","Expert","Legendary"][rarity-1]} {type}"
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
    #TODO based on preliminary testing the scaling could use some work since some randomly created characters
    #are doing ridiculous damage while some do only 1
    scaling = [0,1.01,1.025,1.04,1.06] # 1.01 for common enemies, 1.025 for rare and so on
    stats = {}

    #Randomly generate a starting value for each stat based on type
    if type == "warrior": # HP > atk > magic
        stats["hp"] = randint(25,40)
        stats["atk"] = randint(4,10)
        stats["magic"] = randint(1,5)
    elif type == "rogue": # atk > HP = magic
        stats["hp"] = randint(15,30)
        stats["atk"] = randint(7,14)
        stats["magic"] = randint(3,8)
    else: #mage   magic >> atk = HP
        stats["hp"] = randint(6,24)
        stats["atk"] = randint(1,6)
        stats["magic"] = randint(9,18)

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
    damage = randint(1,5) * 0.2 * rarity * level 
    defense = randint(1,5) * 0.2 * rarity * level
    if type == "warrior":
        wstats = [int(damage*randint(8,12)*0.1),int(damage*randint(1,12)*0.1)]
        astats = [int(defense*randint(8,12)*0.1),int(defense*randint(1,12)*0.1)]
    elif type == "rogue":
        wstats = [int(damage*randint(10,14)*0.1),int(damage*randint(6,12)*0.1)]
        astats = [int(defense*randint(10,14)*0.1),int(defense*randint(6,12)*0.1)]
    else: #mage
        wstats = [damage*randint(1,12)*0.1,damage*randint(8,16)*0.1]
        astats = [defense*randint(1,12)*0.1,defense*randint(8,16)*0.1]
    weapon = Equipment("weapon",wstats,weapon_desc)
    armour = Equipment("armour",astats,armour_desc)
    return [weapon,armour]

def create_skill(type: str, rarity: int):
    """
    type: warrior/rogue/mage
    rarity: common, rare, epic, legendary represented by 1,2,3,4 respectively

    Returns: Skill object 
    """
    # Makes the skill hit every target with 1 in 3 chance
    if randint(1,3) == 1:
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

    multiplier = 0.1 * randint(1,10) * rarity + 1
    if ally:
        multiplier *= -0.8
    if aoe:
        multiplier *= 0.5
    uses = randint(5,10)-rarity
    if aoe:
        aoe="All"
    else:
        aoe="Single"
    name = f"{stat} {multiplier} {aoe}"
    description = "todo"
    # TODO generate name and description based on type, rarity, stat, aoe and ally

    return Skill(name,multiplier,stat,uses,description,ally,aoe)

def battle(players :list,enemies :list):
    """
    players: list consisting of player character and possible allies
    enemies: list of enemies

    Returns:
    "victory" if battle is won
    "defeat" if battle is lost
    "run" if player wishes to try to run away
    """
    #TODO Using skills doesn't currently consume skill uses.
    #TODO enemies don't have a turn yet
    #TODO normal attacks don't work
    #TODO single target skills are hitting all enemies / healing all allies
    dead_enemies = 0
    dead_players = 0
    while True: #Loop that breaks when all enemies or players are dead
        #Ask the player to take action with each ally character
        for player in players:
            sleep(1)
            if len(enemies) - dead_enemies <= 0:
                for enemy in enemies:
                    for player in players:
                        player.gain_exp(enemy.given_exp)
                return "victory"
            #Print the names, level and hp of all combatants at the start of every turn
            print("\nYour Party")
            for p in players:
                print(f"{p.name} LVL {p.level}:  HP: {p.stats['hp']}/{p.stats['hp']+p.lost_hp}")
            print("\nEnemy Party")
            for e in enemies:
                print(f"{e.name}: LVL {e.level}  HP: {e.stats['hp']}/{e.stats['hp']+e.lost_hp}")
            print("\n")
            if player.alive:
                while True: #breaks once player does an action
                    print("Attack:  1\nSkill:  2\nRun:  3\n")
                    #use item can be implemented later if we want
                    action = input(f"Choose action for {player.name}:")
                    while action not in ["1","2","3"]:
                        action = input("Please type 1, 2 or 3: ")
                    if action == "3":
                        for enemy in enemies:
                            for player in players:
                                if not enemy.alive:
                                    player.gain_exp(enemy.given_exp)
                        return "run"
                        #let the llm decide if it succeeds, if llm is bad at it random chance can be implemented
                        #there is an exploit if you have many party members to attack with others and run with the
                        #last one since players always start the battle assuming the battle will continue as it was

                    elif action == "2": # Everything under this elif could be put to its own function since it's quite long
                        #Print the characters skills and prompt the player to choose one
                        counter = 1
                        print("\n")
                        for skill in player.skills:
                            print(f"{skill.name}:  {counter}")
                            counter += 1
                        print(f"Back:  {counter}")
                        try:
                            while True:
                                skill = int(input("Choose skill:"))
                                if skill not in range(1,counter+1):
                                    print("Invalid choice")
                                else:
                                    break
                        except ValueError:
                            print("Invalid input\n")
                            continue
                        if skill == counter: #back was chosen
                            continue
                        skill = player.skills[skill-1]
                        if skill.ally:
                            # currently only healing skills work for self targeting skills
                            # various buffing skills can be implemented later if we wish
                            if skill.stat == "atk":
                                heal = int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier)
                            else:
                                heal = int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier)
                            if skill.aoe or len(players)-dead_players <= 1:
                                for player in players:
                                    if player.alive:
                                        player.take_damage(heal)
                                        print(f"{player.name} was healed for {-heal}")
                            else:
                                # Promt player to select which character to heal
                                counter = 1
                                print("\n")
                                for player in players:
                                    print(f"{player.name} HP:{player.stats['hp']}/{player.stats['hp']+player.lost_hp}:  {counter}")
                                    counter += 1
                                print(f"Back:  {counter}")
                                try:
                                    while True:
                                        target = int(input("Choose target:"))
                                        if target not in range(1,counter+1):
                                            print("Invalid target")
                                        else:
                                            break
                                except ValueError:
                                    print("Invalid input\n")
                                    continue
                                if target == counter: #back was chosen
                                    continue
                                target = players[target-1]
                                if target.alive:
                                    target.take_damage(heal)
                                    print(f"{player.name} was healed for {-heal}")
                                else:
                                    print("Fallen characters cannot be healed")
                                    continue
                        else: #skill is a damaging skill
                            #currently only damaging skills work, debuffs can be implemented later
                            if skill.aoe or len(enemies)-dead_enemies <= 1:
                                for enemy in enemies:
                                    if enemy.alive:
                                        if skill.stat == "atk":
                                            damage = max(1,int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier-enemy.armour.stats[0]))
                                        else:
                                            damage = max(1,int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier-enemy.armour.stats[0]))
                                        if enemy.take_damage(damage) == "dead":
                                            print(f"{enemy.name} took {damage} damage and was defeated")
                                            dead_enemies += 1
                                        else:
                                            print(f"{enemy.name} took {damage} damage")
                            else: # Skill is single target
                                # Promt player to select which enemy to attack
                                counter = 1
                                print("\n")
                                for enemy in enemies:
                                    print(f"{enemy.name} HP:{enemy.stats['hp']}/{enemy.stats['hp']+enemy.lost_hp}:  {counter}")
                                    counter += 1
                                print(f"Back:  {counter}")
                                try:
                                    while True:
                                        target = int(input("Choose target:"))
                                        if target not in range(1,counter+1):
                                            print("Invalid target")
                                        else:
                                            break
                                except ValueError:
                                    print("Invalid input\n")
                                    continue
                                if target == counter: #back was chosen
                                    continue
                                target = enemies[target-1]
                                if target.alive:
                                    if skill.stat == "atk":
                                        damage = max(1,int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier-enemy.armour.stats[0]))
                                    else:
                                        damage = max(1,int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier-enemy.armour.stats[0]))
                                    if target.take_damage(damage) == "dead":
                                        print(f"{target.name} took {damage} damage and was defeated")
                                        dead_enemies += 1
                                    else:
                                        print(f"{enemy.name} took {damage} damage")
                                else:
                                    print("Fallen enemies cannot be attacked")
                                    continue
                        break #getting to this line should mean a skill has been successfully used
                    else: # action is "3" as in a normal attack
                        print(f"{player.name} fails to act")
                        break
                        #work in progress
        for enemy in enemies:
            if enemy.alive:
                damage = max(1,int(enemy.stats["atk"]+enemy.weapon.stats[0]-players[0].armour.stats[0]))                 
                if players[0].take_damage(damage) == "dead":
                    print(f"{players[0].name} took {damage} damage and was defeated")
                    dead_players += 1
                else:
                    print(f"{players[0].name} took {damage} damage")
                sleep(1)
                if len(players) - dead_players <= 0:
                    return "defeat"
                #work in progress, can only attack main character and use normal attacks

player_party = create_enemies(25,8)
for i in range(5,9):
    level = player_party[0].level
    enemy_party = create_enemies(level,i)
    if battle(player_party,enemy_party) != "victory":
        print("Better luck next time")
        break
    else:
        print(f"You have defeated difficulty {i}. {8-i} battles remain")
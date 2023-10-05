class Character():
    def __init__(self, name :str, stats :dict, level :int, description :str):
        """ Used for both playable and npc characters. """
        self.name = name
        self.stats = stats
        self.multipliers = None # necessary for leveling up, only relevant for playable characters
        self.level = level
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
            if self.exp >= self.level * 10:
                self.exp -= self.level * 10
                self.level += 1
                self.stats["hp"] += self.lost_hp
                self.lost_hp = 0
                self.stats["hp"] = int(self.multipliers["hp"] * self.stats["hp"])
                self.stats["atk"] = int(self.multipliers["atk"] * self.stats["atk"])
                self.stats["magic"] = int(self.multipliers["magic"] * self.stats["magic"])
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
from random import randint
from time import sleep
def battle(players :list,enemies :list):
    """
    players: list consisting of player character and possible allies
    enemies: list of enemies

    Returns:
    "victory" if battle is won
    "defeat" if battle is lost
    "run" if player wishes to try to run away
    """
    #Using skills doesn't currently consume skill uses. This should be fixed eventually.
    #Also enemies don't have a turn yet
    #Also also normal attacks don't work
    dead_enemies = 0
    dead_players = 0
    while True: #Loop that breaks when all enemies or players are dead
        if len(enemies) - dead_enemies <= 0:
            for enemy in enemies:
                for player in players:
                    player.gain_exp(enemy.given_exp)
            return "victory"
        if len(players) - dead_players <= 0:
            return "defeat"
        #Print the names and hp of all combatants at the start of every round
        print("\nYour Party")
        for player in players:
            print(f"{player.name}:  HP: {player.stats['hp']}/{player.stats['hp']+player.lost_hp}")
        print("\nEnemy Party")
        for enemy in enemies:
            print(f"{enemy.name}:  HP: {enemy.stats['hp']}/{enemy.stats['hp']+enemy.lost_hp}")
        print("\n")
        #Ask the player to take action with each ally character
        for player in players:
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
                #work in progress, can only attack main character and use normal attacks

hero_party = [create_main_character()]
goblin_party = create_goblins()

print(battle(hero_party,goblin_party))
second_wave = create_goblins()
print(battle(hero_party,second_wave))
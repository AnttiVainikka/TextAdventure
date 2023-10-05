from Characters.equipment import Equipment
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

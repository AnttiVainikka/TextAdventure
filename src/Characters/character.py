class Character():
    def __init__(self, name :str, stats :dict, level :int, description :str):
        """ Used for both playable and npc characters."""
        self.name = name
        self.stats = stats
        self.level = level
        self.exp = 0
        self.skills = []
        self.weapon = None
        self.armour = None
        self.description = description
        self.alive = True
        self.enemy = False #change to True if npc turns hostile to player
        # self.skillset could be implemented to have character learn specific skills
        # at specific levels 
    
    def gain_exp(self,exp):
        """ Each level up takes current level * 10 experience. Max level
        is 10. Can be changed later. """
        self.exp += exp
        while True:
            if self.level >= 10:
                break
            if self.exp >= self.level * 10:
                self.exp -= self.level * 10
                self.level += 1
            else:
                break

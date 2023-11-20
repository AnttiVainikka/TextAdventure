from Characters.equipment import Equipment, EquipmentType
from Journey.utility import to_dict
from Characters.skill import Skill

class Character():
    def __init__(self, kind :str, name :str, stats :dict, multipliers :int, description :str, type :str = "Warrior", race :str = "Human"):
        """ Used for both playable and npc characters. """
        self.kind = kind
        self.name = name
        self.race = race
        self.stats = stats
        self.multipliers = multipliers
        self.level = 1
        self.exp = 0
        self.skills = []
        self.weapon = Equipment(EquipmentType.Weapon)
        self.armour = Equipment(EquipmentType.Armour)
        self.description = description
        self.alive = True
        self.lost_hp = 0
        self.given_exp = 0 # how much exp enemy gives when defeated
        self.enemy = False #change to True if npc turns hostile to player
        self.type = type
        self.inventory = []
        # self.skillset could be implemented to have character learn specific skills
        # at specific levels
    
    def __init_from_dict__(self, state: dict):
        self.kind = state["kind"]
        self.name = state["name"]
        self.stats = state["stats"]
        self.multipliers = state["multipliers"]
        self.level = state["level"]
        self.exp = state["exp"]
        self.skills = [Skill.create_from_dict(skill) for skill in state["skills"]]
        self.weapon = Equipment.create_from_dict(state["weapon"])
        self.armour = Equipment.create_from_dict(state["armour"])
        self.description = state["description"]
        self.alive = state["alive"]
        self.lost_hp = state["lost_hp"]
        self.given_exp = state["given_exp"]
        self.enemy = state["enemy"]
        self.type = state["type"]
        self.race = state["race"]
        self.inventory = [Equipment.create_from_dict(equipment) for equipment in state["inventory"]]

    def create_from_dict(state: dict) -> "Character":
        if state is None: return None
        character = Character.__new__(Character)
        character.__init_from_dict__(state)
        return character

    def to_dict(self) -> dict:
        return {
            "kind": to_dict(self.kind),
            "name": to_dict(self.name),
            "race": to_dict(self.race),
            "stats": to_dict(self.stats),
            "multipliers": to_dict(self.multipliers),
            "level": to_dict(self.level),
            "exp": to_dict(self.exp),
            "skills": to_dict(self.skills),
            "weapon": to_dict(self.weapon),
            "armour": to_dict(self.armour),
            "description": to_dict(self.description),
            "alive": to_dict(self.alive),
            "lost_hp": to_dict(self.lost_hp),
            "given_exp": to_dict(self.given_exp),
            "enemy": to_dict(self.enemy),
            "type": to_dict(self.type),
            "inventory": to_dict(self.inventory)
        }

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

    @property
    def max_hp(self) -> int:
        return self.stats["hp"] + self.lost_hp

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
    
    def heal_percent(self, percent: float):
        heal_value = int(self.max_hp * percent)
        self.stats["hp"] += min(self.lost_hp, heal_value)
        self.lost_hp = max(0, self.lost_hp - heal_value)

    def damage_percent(self, percent: float):
        damage_value = int(self.max_hp * percent)
        self.take_damage(damage_value)

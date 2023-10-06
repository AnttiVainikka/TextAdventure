from faction import Faction
from Characters.equipment import Equipment

test_reward = Equipment(
  type = "Armour",
  stats = [3, "Heavy"],
  description = "A heavy breastplate"
)

test_faction = Faction(
  name = "Wizard guild",
  description = "A guild of wizards who wizard about",
  location = "Outskirts",
  setting = "A group of tents east of Bad Goblin Forest and North of Another Bandit Lair",
  reward = test_reward)


print(test_faction)
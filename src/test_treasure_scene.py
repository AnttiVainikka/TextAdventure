#connect to LLM
from Journey.TreasurePlay import TreasurePlay
from Journey.TreasureScene import TreasureScene
from Journey.Intuition import Intuitions

intuitions = Intuitions([
    "You are somewhere in a forest",
    "You have defeated some goblins"
])

scene = TreasureScene(None, 2, intuitions)
play = scene.play
interaction = play.interact
print(interaction)
interaction = interaction(1)

print("--------------------------------------------\n")
print(interaction)

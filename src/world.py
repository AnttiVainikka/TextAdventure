from dataclasses import dataclass
from pathlib import Path
import pickle

from Generation.faction import Faction
from Generation.scenario import Scenario

@dataclass
class GameWorld:
    scenario: Scenario
    factions: list[Faction]

def save_world(name: str, world: GameWorld) -> None:
    Path('saves').mkdir(exist_ok=True)
    with open(f'saves/{name}.wld', 'wb') as f:
        pickle.dump(world, f)

def load_world(name: str) -> GameWorld:
    with open(f'saves/{name}.wld', 'rb') as f:
        return pickle.load(f)
from typing import TYPE_CHECKING

from Generation.area import Area
from Generation.battle_scene import generate_enemy_types, generate_legendary_enemy, EnemyType

from Journey.Scenes.Scene import Scene
from Journey.Plays.BattlePlay import BattlePlay
from Journey.Difficulty import Difficulty
from Journey.utility import to_dict

if TYPE_CHECKING:
    from Journey.Layout import Layout

class BattleScene(Scene):
    # TODO: Integrate battle 
    def __init__(self, parent: "Layout", area: Area, difficulty: Difficulty):
        super().__init__(parent, area, difficulty)
        self._enemy_types = generate_enemy_types(parent.name, parent.description, area.name, area.description)
        self._leader = generate_legendary_enemy(parent.name, parent.description, area.name, area.description, self._enemy_types[0]) \
                                                if difficulty == Difficulty.Challenging else None
        self._plays.append(BattlePlay(self, parent.name, parent.description, area, self._enemy_types, self._leader))

    def __init_from_dict__(self, parent: "Layout", state: dict):
        super().__init_from_dict__(parent, state)
        self._enemy_types = [EnemyType(**enemy_type) for enemy_type in state["enemy_types"]]
        self._leader = EnemyType(**state["leader"]) if state["leader"] is not None else None

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["enemy_types"] = [to_dict(enemy_type) for enemy_type in self._enemy_types]
        state["leader"] = to_dict(self._leader)
        return state

    def _next(self) -> "BattlePlay":
        return self._plays[0]

    def has_next(self) -> bool:
        return self._current_play != self._plays[0]

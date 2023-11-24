from typing import TYPE_CHECKING

from battle import battle

from Characters.create import create_enemies
from Characters.character import Character

from Generation.area import Area
from Generation.enemy_type import generate_epic_enemy, generate_from_region, EnemyType
from Journey.Action import PlayFinishedAction, StartBattleAction

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
        self._enemy_types = generate_from_region(parent.name, parent.description, area.name, area.description)
        self._leader = generate_epic_enemy(parent.name, parent.description, area.name, area.description, self._enemy_types[0]) \
                                                if difficulty == Difficulty.Challenging else None
        self._plays.append(BattlePlay(self, parent.name, parent.description, area, self._enemy_types, self._leader))

    def __init_from_dict__(self, parent: "Layout", state: dict):
        super().__init_from_dict__(parent, state)
        self._enemy_types = [EnemyType.create_from_dict(enemy_type) for enemy_type in state["enemy_types"]]
        self._leader = EnemyType.create_from_dict(state["leader"])

    def _process_StartBattleAction(self, action: StartBattleAction):
        play = action.play
        if play == self._current_play:
            real_enemy_types = self._enemy_types
            if self._leader is not None:
                real_enemy_types.append(self._leader)
            enemies = create_enemies(self.parent.parent.character.level, self.difficulty.value, 
                                     real_enemy_types)
            battle([self.parent.parent.character, *self.parent.parent.character.party_members], enemies)


    def to_dict(self) -> dict:
        state = super().to_dict()
        state["enemy_types"] = [to_dict(enemy_type) for enemy_type in self._enemy_types]
        state["leader"] = to_dict(self._leader)
        return state

    def _next(self) -> "BattlePlay":
        return self._plays[0]

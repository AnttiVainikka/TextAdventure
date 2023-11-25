from typing import TYPE_CHECKING

from Characters.create import create_enemies

from Generation.area import Area
from Generation.enemy_type import generate_boss, EnemyType

from Journey.Scenes.Scene import Scene
from Journey.Plays.FinalBattlePlay import FinalBattlePlay
from Journey.Difficulty import Difficulty
from Journey.utility import to_dict

from Journey.Action import StartBattleAction
from battle import battle

if TYPE_CHECKING:
    from Journey.Layout import Layout

class FinalBattleScene(Scene):
    # TODO: Integrate battle 
    def __init__(self, parent: "Layout", area: Area, difficulty: Difficulty):
        super().__init__(parent, area, difficulty)
        self._boss = generate_boss(parent.name, area.name, area.description, parent.mission.quest_description)
        self._plays.append(FinalBattlePlay(self, parent.name, parent.mission.description, area, self._boss))

    def __init_from_dict__(self, parent: "Layout", state: dict):
        super().__init_from_dict__(parent, state)
        self._boss = EnemyType.create_from_dict(state["boss"])

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["boss"] = to_dict(self._boss)
        return state

    def _process_StartBattleAction(self, action: StartBattleAction):
        play = action.play
        if play == self._current_play:
            enemies = create_enemies(self.parent.parent.character.level, 3 * self.difficulty.value, 
                                     [self._boss])
            result = battle([self.parent.parent.character, *self.parent.parent.character.party_members], enemies)

    def _next(self) -> "FinalBattlePlay":
        return self._plays[0]

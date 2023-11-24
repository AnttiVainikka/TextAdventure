from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.Scenes.Scene import Scene
from Journey.Plays.RiddlePlay import RiddlePlay
from Journey.Difficulty import Difficulty
from Journey.Action import (
    RiddleWrongAnswerAction,
    RiddleGoodAnswerAction,
    ExpAction,
    DamageAction,
    SceneFinishedAction
)

if TYPE_CHECKING:
    from Journey.Layout import Layout

class RiddleScene(Scene):
    _DIFFICULTY_TO_EXP = {
        Difficulty.Easy: 5,
        Difficulty.Normal: 10,
        Difficulty.Hard: 20,
        Difficulty.Challenging: 50
    }

    _DIFFICULTY_TO_DAMAGE = {
        Difficulty.Easy: 0.01,
        Difficulty.Normal: 0.02,
        Difficulty.Hard: 0.03,
        Difficulty.Challenging: 0.04
    }

    def __init__(self, parent: "Layout", area: Area, difficulty: Difficulty):
        super().__init__(parent, area, difficulty)
        self._plays.append(RiddlePlay(self, parent.name, parent.description, area, difficulty))

    def _next(self) -> "RiddlePlay":
        return self._plays[0]

    def _process_RiddleWrongAnswerAction(self, action: RiddleWrongAnswerAction):
        self._raise_action(DamageAction(self, RiddleScene._DIFFICULTY_TO_DAMAGE[self._difficulty]))

    def _process_RiddleGoodAnswerAction(self, action: RiddleGoodAnswerAction):
        self._raise_action(ExpAction(self, RiddleScene._DIFFICULTY_TO_EXP[self._difficulty]))
        self._raise_action(SceneFinishedAction(self))

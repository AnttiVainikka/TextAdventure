from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.Scenes.Scene import Scene
from Journey.Plays.IntroPlay import IntroPlay
from Journey.Difficulty import Difficulty
from Journey.Action import IntroLeaveAction, IntroEnterAction, SceneFinishedAction, ReturnToCapitalAction, EnterRegionAction

if TYPE_CHECKING:
    from Journey.Layout import Layout

class IntroScene(Scene):
    def __init__(self, parent: "Layout", area: Area, difficulty: Difficulty = Difficulty.Easy):
        super().__init__(parent, area, difficulty)
        self._plays.append(IntroPlay(self, self._parent.name, self._parent.description, self._parent.capital, parent.mission.description))

    def _next(self) -> "IntroPlay":
        return self._plays[0]

    def _process_IntroLeaveAction(self, action: "IntroLeaveAction"):
        self.stop()
        self._raise_action(ReturnToCapitalAction(self))

    def _process_IntroEnterAction(self, action: "IntroEnterAction"):
        self.stop()
        self._raise_action(EnterRegionAction(self))

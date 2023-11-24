from typing import TYPE_CHECKING

from Journey.Scenes.Scene import Scene
from Journey.Plays.OutroPlay import OutroPlay
from Journey.Difficulty import Difficulty
from Journey.Action import PlayFinishedAction, ReturnToCapitalAction, SceneFinishedAction

if TYPE_CHECKING:
    from Journey.Layout import Layout

class OutroScene(Scene):
    def __init__(self, parent: "Layout"):
        super().__init__(parent, None, Difficulty.Easy)
        self._plays.append(OutroPlay(self, parent.name, parent.capital, parent.mission.description))

    def _next(self) -> "OutroPlay":
        return self._plays[0]

    def _process_PlayFinishedAction(self, action: PlayFinishedAction):
        if action.play == self._plays[0]:
            self._raise_action(SceneFinishedAction(self))

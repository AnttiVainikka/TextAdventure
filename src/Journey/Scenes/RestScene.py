from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.Scenes.Scene import Scene
from Journey.Plays.RestPlay import RestPlay
from Journey.Difficulty import Difficulty
from Journey.Action import (
    SkipAction,
    RefillHPAction,
    RestAction,
    SceneFinishedAction
)

if TYPE_CHECKING:
    from Journey.Layout import Layout

class RestScene(Scene):
    def __init__(self, parent: "Layout", area: Area, difficulty: Difficulty):
        super().__init__(parent, area, difficulty)
        self._plays.append(RestPlay(self, parent.name, parent.description, area))

    def _next(self) -> "RestPlay":
        return self._plays[0]

    def _process_SkipAction(self, action: SkipAction):
        self._raise_action(SceneFinishedAction(self))

    def _process_RestAction(self, action: RestAction):
        self._raise_action(RefillHPAction(self, 1.0))
        self._raise_action(SceneFinishedAction(self))

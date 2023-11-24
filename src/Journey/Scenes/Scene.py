from abc import abstractmethod
from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import ActionConcern
from Journey.Difficulty import Difficulty
from Journey.Plays import create_from_dict as create_play
from Journey.utility import to_dict, to_dict_index
from Journey.Action import PlayFinishedAction, SceneFinishedAction
from Journey.LoopManager import LoopManager

if TYPE_CHECKING:
    from Journey.Plays.Play import Play
    from Journey.Layout import Layout

class Scene(BaseActionComponent, LoopManager):
    def __init__(self, parent: "Layout", area: Area, difficulty: "Difficulty"):
        BaseActionComponent.__init__(self, parent, ActionConcern.Scene)
        LoopManager.__init__(self)
        self._area = area
        self._difficulty: Difficulty = difficulty
        self._plays: list[Play] = []
        self._current_play: Play = None

    def __init_from_dict__(self, parent: "Layout", state: dict):
        BaseActionComponent.__init__(self, parent, ActionConcern.Scene)
        LoopManager.__init__(self)
        self._area = Area(**state["area"]) if state["area"] is not None else None
        self._difficulty = Difficulty[state["difficulty"]]
        self._plays = [create_play(self, play_state) for play_state in state["plays"]]
        self._current_play = None if state["current_play"] is None \
                             else self._plays[state["current_play"]]

    def to_dict(self) -> dict:
        return {
            "type": to_dict(type(self).__name__),
            "area": to_dict(self._area),
            "difficulty": to_dict(self._difficulty.name),
            "plays": [to_dict(play) for play in self._plays],
            "current_play": to_dict_index(self._current_play, self._plays)
        }

    @property
    def area(self) -> Area:
        return self._area

    @property
    def difficulty(self) -> "Difficulty":
        return self._difficulty

    @property
    def play(self) -> "Play":
        return self._current_play

    def _do_work(self):
        play = self.next()
        play.run()

    def next(self) -> "Play":
        self._current_play = self._next()
        return self._current_play
    
    def stop(self):
        self._current_play.stop()
        super().stop()

    def _process_PlayFinishedAction(self, action: PlayFinishedAction):
        play = action.play
        if play == self._current_play:
            self._current_play.stop()
            if len(self._plays) == 1:
                self._raise_action(SceneFinishedAction(self))

    @abstractmethod
    def _next(self) -> "Play":
        pass

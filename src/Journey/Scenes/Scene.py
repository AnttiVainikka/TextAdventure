from abc import abstractmethod
from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import ActionConcern
from Journey.Difficulty import Difficulty
from Journey.Plays import create_from_dict as create_play
from Journey.utility import to_dict, to_dict_index

if TYPE_CHECKING:
    from Journey.Plays.Play import Play
    from Journey.Layout import Layout

class Scene(BaseActionComponent):
    def __init__(self, parent: "Layout", area: Area, difficulty: "Difficulty"):
        super().__init__(parent, ActionConcern.Scene)
        self._area = area
        self._difficulty: Difficulty = difficulty
        self._plays: list[Play] = []
        self._current_play: Play = None

    def __init_from_dict__(self, parent: "Layout", state: dict):
        super().__init__(parent, ActionConcern.Scene)
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
    def is_finished(self) -> bool:
        return self._current_play is not None and self._current_play.is_finished and \
               not self.has_next()

    @property
    def play(self) -> "Play":
        return self._current_play

    def next(self) -> "Play":
        if (self._current_play is None or
           (self._current_play.is_finished and self.has_next())):
            self._current_play = self._next()
        return self._current_play
    
    def reset(self):
        self._current_play = None
        for play in self._plays:
            play.reset()

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def _next(self) -> "Play":
        pass

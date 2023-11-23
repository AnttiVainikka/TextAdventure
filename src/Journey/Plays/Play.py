from abc import abstractmethod
from typing import TYPE_CHECKING
import time

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Interaction import Interaction
from Journey.Action import ActionConcern
from Journey.utility import to_dict, to_dict_index
from Journey.LoopManager import LoopManager

if TYPE_CHECKING:
    from Journey.Scenes.Scene import Scene

_TEXT_DISPLAY_SPEED = 0.00

Input = input

def UserInput():
    return input(f"Player: ")

def Output(msg: str):
    print("\n")
    print("-"*80)
    print("\n")
    for char in msg:
        print(char, end='', flush=True)
        time.sleep(_TEXT_DISPLAY_SPEED)
    print("\n")


class Play(BaseActionComponent, LoopManager):
    def __init__(self, parent: "Scene"):
        BaseActionComponent.__init__(self, parent, ActionConcern.Play)
        LoopManager.__init__(self)
        self._parent = parent
        self._interactions: list[Interaction] = []
        self._current_interaction = None

    def __init_from_dict__(self, parent: "Scene", state: dict):
        BaseActionComponent.__init__(self, parent, ActionConcern.Play)
        LoopManager.__init__(self)
        self._interactions = [Interaction.create_from_dict(self, interaction) for interaction in state["interactions"]]
        self._current_interaction = None if state["current_interaction"] is None \
                                    else self._interactions[state["current_interaction"]]

    def to_dict(self) -> dict:
        return {
            "type": to_dict(type(self).__name__),
            "interactions": [to_dict(interaction) for interaction in self._interactions],
            "current_interaction": to_dict_index(self._current_interaction, self._interactions)
        }

    @property
    def interaction(self) -> "Interaction":
        return self._current_interaction

    def _do_work(self):
        interaction = self.next()
        Output(str(interaction))
        if interaction.is_info:
            interaction(Input("Press enter to continue..."))
        else:
            interaction(UserInput())

    def next(self) -> "Interaction":
        self._current_interaction = self._next()
        self._current_interaction.restart()
        return self._current_interaction

    @abstractmethod
    def _next(self) -> "Interaction":
        pass

from abc import abstractmethod
from typing import TYPE_CHECKING

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Interaction import Interaction
from Journey.Action import ActionConcern
from Journey.utility import to_dict, to_dict_index

if TYPE_CHECKING:
    from Journey.Scenes.Scene import Scene

class Play(BaseActionComponent):
    def __init__(self, parent: "Scene"):
        super().__init__(parent, ActionConcern.Play)
        self._parent = parent
        self._interactions: list[Interaction] = []
        self._current_interaction = None

    def __init_from_dict__(self, parent: "Scene", state: dict):
        super().__init__(parent, ActionConcern.Play)
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
    def is_finished(self) -> bool:
        return self._current_interaction is not None and \
               self._current_interaction.is_answered and not self.has_next()

    @property
    def interaction(self) -> "Interaction":
        return self._current_interaction

    def next(self) -> "Interaction":
        if (self._current_interaction is None or 
           (self._current_interaction.is_answered and self.has_next())):
            self._current_interaction = self._next()
        return self._current_interaction

    def reset(self):
        self._current_interaction = None
        for interaction in self._interactions:
            if interaction is not None: interaction.reset()

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def _next(self) -> "Interaction":
        pass

from typing import TYPE_CHECKING
from enum import Enum

from Journey.Plays.Play import Play
from Journey.Interaction import QSAInteraction

from Journey.Action import InteractionAnsweredAction, RegionSelectionAction, FactionSelectionAction

if TYPE_CHECKING:
    from Journey.Scenes.IntroScene import IntroScene

class MainChoice(Enum):
    SELECT_REGION = 1
    SELECT_FACTION = 2

class MainPlay(Play):
    def __init__(self, parent: "IntroScene"):
        super().__init__(parent)
        self._choices = {
            MainChoice.SELECT_REGION.value: "Select region...",
            MainChoice.SELECT_FACTION.value: "Select faction..."
        }

        self._interactions.append(QSAInteraction(self, "Where do you want to go?", self._choices))

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0] and interaction.is_answered:
            if interaction.answer == MainChoice.SELECT_REGION.value:
                self._raise_action(RegionSelectionAction(self))
            else:
                self._raise_action(FactionSelectionAction(self))

    def has_next(self):
        return self._interactions[0] != self._current_interaction

    def _next(self) -> QSAInteraction:
        return self._interactions[0]

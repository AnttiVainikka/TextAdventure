from typing import TYPE_CHECKING
from enum import Enum

from Generation.intro_scene import generate

from Journey.Interaction import QSAInteraction
from Journey.Plays.Play import Play
from Journey.Interaction import Interaction
from Journey.Action import (
    IntroEnterAction,
    IntroLeaveAction,
    InteractionAnsweredAction
)

if TYPE_CHECKING:
    from Journey.Scenes.IntroScene import IntroScene

class IntroChoice(Enum):
    ENTER = 1
    RETURN = 2

class IntroPlay(Play):
    def __init__(self, parent: "IntroScene", region_name: str, region_description: str, capital_name: str, mission: str):
        super().__init__(parent)
        context = generate(region_name, region_description, mission)
        self._interactions = [QSAInteraction(self, context, {IntroChoice.ENTER.value: f"Enter to {region_name}",
                                                             IntroChoice.RETURN.value: f"Return to {capital_name}"})]
    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0] and interaction.is_answered:
            if interaction.answer == IntroChoice.ENTER.value:
                self._raise_action(IntroEnterAction(self))
            else:
                self._raise_action(IntroLeaveAction(self))

    def has_next(self):
        return self._interactions[0] != self._current_interaction

    def _next(self) -> Interaction:
        return self._interactions[0]

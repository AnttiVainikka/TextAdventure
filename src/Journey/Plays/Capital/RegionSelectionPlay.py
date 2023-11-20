from typing import TYPE_CHECKING

from Journey.Plays.Play import Play
from Journey.Interaction import QSAInteraction

from Journey.Action import InteractionAnsweredAction, SelectedRegionAction

if TYPE_CHECKING:
    from Journey.Scenes.IntroScene import IntroScene

class RegionSelectionPlay(Play):
    def __init__(self, parent: "IntroScene", region_names: list[str]):
        super().__init__(parent)
        self._choices = {
            i + 1: region_name for (i, region_name) in enumerate(region_names)
        }

        self._interactions.append(QSAInteraction(self, "Where do you want to go?", self._choices))

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0] and interaction.is_answered:
            self._raise_action(SelectedRegionAction(self, interaction.answer))

    def has_next(self):
        return self._interactions[0] != self._current_interaction

    def _next(self) -> QSAInteraction:
        return self._interactions[0]

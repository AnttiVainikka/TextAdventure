from typing import TYPE_CHECKING

from Journey.Plays.Play import Play
from Journey.Interaction import QSAInteraction

from Journey.Action import InteractionAnsweredAction, SelectedFactionAction

if TYPE_CHECKING:
    from Journey.Scenes.IntroScene import IntroScene

class FactionSelectionPlay(Play):
    def __init__(self, parent: "IntroScene", faction_names: list[str]):
        super().__init__(parent)
        choices = {
            i + 1: faction_name for (i, faction_name) in enumerate(faction_names)
        }

        self._interactions.append(QSAInteraction(self, "Who do you want to talk to?", choices))

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0] and interaction.is_answered:
            self._raise_action(SelectedFactionAction(self, interaction.answer))

    def _next(self) -> QSAInteraction:
        return self._interactions[0]

from typing import TYPE_CHECKING

from Journey.Plays.Play import Play
from Journey.Interaction import QSAInteraction

from Journey.Action import InteractionAnsweredAction, SelectionAction

from Journey.utility import to_dict

if TYPE_CHECKING:
    from Journey.Scenes.Scene import Scene

class SelectionPlay(Play):
    def __init__(self, parent: "Scene",
                 question: str,
                 values: list[str] | dict,
                 back: (int, str) = (0, "Back")):
        super().__init__(parent)
        choices = {}
        if isinstance(values, list): 
            choices = {
                i + 1: value for (i, value) in enumerate(values)
            }
        else:
            choices = values

        if back is not None:
            choices[back[0]] = back[1]

        self._interactions.append(QSAInteraction(self, question, choices))
        self._current_interaction = self._interactions[0]

    def remove(self, value_to_remove: str):
        interaction = self.interaction
        key = interaction.answer_to_key(value_to_remove)
        if key is not None:
            interaction.remove_answer(key)

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0] and interaction.is_answered:
            self._raise_action(SelectionAction(self, interaction.answer, interaction.key_to_answer(interaction.answer)))

    def _next(self) -> QSAInteraction:
        return self._interactions[0]

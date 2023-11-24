from typing import TYPE_CHECKING
from enum import Enum

from Generation.area import Area
from Generation.rest_scene import *

from Journey.Plays.Play import Play
from Journey.Interaction import QSAInteraction, Interaction
from Journey.utility import to_dict
from Journey.Action import (
    InteractionAnsweredAction,
    RestAction,
    SkipAction
)

if TYPE_CHECKING:
    from Journey.Scenes.RestScene import RestScene

class RestChoice(Enum):
    REST = 1
    CONTINUE = 2

class RestPlay(Play):
    _INDEX_CONTEXT = 0
    _INDEX_REST = 1
    _INDEX_LEAVE = 2

    def __init__(self, parent: "RestScene", region_name: str, region_description: str, area: Area):
        super().__init__(parent)
        context = generate_intro_context(region_name, region_description, area.name, area.description)
        rest_context = generate_outro_rest_context(area.name, context)
        leave_context = generate_outro_leave_context(area.name, context)
        self._choices = {
            RestChoice.REST.value: "Rest here for the night and continue next day morning",
            RestChoice.CONTINUE.value: "Continue on your journey"
        }
        self._interactions.append(QSAInteraction(self, context, self._choices))
        self._interactions.append(Interaction(self, rest_context, True))
        self._interactions.append(Interaction(self, leave_context, True))

    def __init_from_dict__(self, parent: "RestScene", state: dict):
        super().__init_from_dict__(parent, state)
        self._choices = {int(key): value for key, value in state["choices"].items()}

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["choices"] = to_dict(self._choices)
        return state

    @property
    def _interaction_context(self) -> "QSAInteraction":
        return self._interactions[RestPlay._INDEX_CONTEXT]

    @property
    def _interaction_rest(self) -> "Interaction":
        return self._interactions[RestPlay._INDEX_REST]
    
    @property
    def _interaction_leave(self) -> "Interaction":
        return self._interactions[RestPlay._INDEX_LEAVE]

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interaction_context:
            if interaction.answer == RestChoice.REST.value:
                self._raise_action(RestAction(self))
            else:
                self._raise_action(SkipAction(self))

    def _next(self) -> Interaction:
        match self._current_interaction:
            case None:
                return self._interaction_context
            
            case self._interaction_context:
                if self._current_interaction.answer == RestChoice.REST.value:
                    return self._interaction_rest
                else:
                    return self._interaction_leave
                
            case _:
                return self._current_interaction
    
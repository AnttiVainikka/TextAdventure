from typing import TYPE_CHECKING
from abc import abstractmethod
from enum import Enum

from Generation.area import Area
from Generation.treasure_scene import *

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction, QSAInteraction
from Journey.utility import to_dict
from Journey.Action import (
    OpenSacrificeChestAction,
    OpenFreeChestAction,
    OpenTrapChestAction,
    LeaveChestAction,
    InteractionAnsweredAction
)

if TYPE_CHECKING:
    from Journey.Scenes.TreasureScene import TreasureScene

class TreasureChoice(Enum):
    OPEN = 1
    CONTINUE = 2

class TreasurePlay(Play):
    _INDEX_CONTEXT = 0
    _INDEX_OPEN = 1
    _INDEX_LEAVE = 2

    def __init__(self, parent: "TreasureScene", context_intro: str, context_open: str, context_leave: str, choices: dict):
        super().__init__(parent)
        self._choices = choices
        self._interactions.append(QSAInteraction(self, context_intro, self._choices))
        self._interactions.append(Interaction(self, context_open, True))
        self._interactions.append(Interaction(self, context_leave, True))

    def __init_from_dict__(self, parent: "TreasureScene", state: dict):
        super().__init_from_dict__(parent, state)
        self._choices = state["choices"]

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["choices"] = to_dict(self._choices)
        return state

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interaction_context:
            if interaction.answer == TreasureChoice.OPEN.value:
                self._raise_action(self._open_action())
            else:
                self._raise_action(self._leave_action())

    @property
    def _interaction_context(self) -> "QSAInteraction":
        return self._interactions[TreasurePlay._INDEX_CONTEXT]

    @property
    def _interaction_open(self) -> "Interaction":
        return self._interactions[TreasurePlay._INDEX_OPEN]
    
    @property
    def _interaction_leave(self) -> "Interaction":
        return self._interactions[TreasurePlay._INDEX_LEAVE]

    def has_next(self) -> bool:
        return self._current_interaction != self._interaction_leave and \
               self._current_interaction != self._interaction_open

    def _next(self) -> Interaction:
        match self._current_interaction:
            case None:
                return self._interaction_context
            
            case self._interaction_context:
                if self._interaction_context.answer == TreasureChoice.OPEN.value:
                    return self._interaction_open
                else:
                    return self._interaction_leave
            
            case _:
                return self._current_interaction

    @abstractmethod
    def _open_action(self):
        pass

    def _leave_action(self):
        return LeaveChestAction(self)

class FreeTreasurePlay(TreasurePlay):
    def __init__(self, parent: "TreasureScene", region_name: str, region_description: str, area: Area, possible_loot: str):
        context_intro = generate_free_intro_context(region_name, region_description, area.name, area.description)
        context_open = generate_free_outro_open_context(area.name, context_intro, possible_loot)
        context_leave = generate_free_outro_leave_context(area.name, context_intro)
        choices = {
            TreasureChoice.OPEN.value: "Open the chest",
            TreasureChoice.CONTINUE.value: "Leave the chest and continue the journey"
        }
        super().__init__(parent, context_intro, context_open, context_leave, choices)

    def _open_action(self):
        return OpenFreeChestAction(self)

class TrapTreasurePlay(TreasurePlay):
    def __init__(self, parent: "TreasureScene", region_name: str, region_description: str, area: Area):
        context_intro = generate_trap_intro_context(region_name, region_description, area.name, area.description)
        context_open = generate_trap_outro_open_context(area.name, context_intro)
        context_leave = generate_trap_outro_leave_context(area.name, context_intro)
        choices = {
            TreasureChoice.OPEN.value: "Open the chest",
            TreasureChoice.CONTINUE.value: "Leave the chest and continue the journey"
        }
        super().__init__(parent, context_intro, context_open, context_leave, choices)

    def _open_action(self):
        return OpenTrapChestAction(self)

class SacrificeTreasurePlay(TreasurePlay):
    def __init__(self, parent: "TreasureScene", region_name: str, region_description: str, area: Area, possible_loot: str):
        context_intro = generate_sacrifice_intro_context(region_name, region_description, area.name, area.description)
        context_open = generate_sacrifice_outro_open_context(area.name, context_intro, possible_loot)
        context_leave = generate_sacrifice_outro_leave_context(area.name, context_intro)
        choices = {
            TreasureChoice.OPEN.value: f"Sacrifice a portion of your hp and open the chest",
            TreasureChoice.CONTINUE.value: "Leave the chest and continue the journey"
        }
        super().__init__(parent, context_intro, context_open, context_leave, choices)

    def _open_action(self):
        return OpenSacrificeChestAction(self)
    
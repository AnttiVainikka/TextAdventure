from enum import Enum
from Journey.Play import Play
from Generation import treasure_play as play_generation
from Journey.Interaction import Interaction

class TreasurePlay(Play):
    _LEAVING_LOOT_TEXT = "Nothing, because the player is leaving"
    _CHOICE_LOOT = 1
    _CHOICE_LEAVE = 2

    def __init__(self, parent):
        super().__init__(parent)
        self._choices = {}
        self._current_interaction = None

    def _generate_next_interaction(self) -> Interaction:
        if self._current_interaction is None:
            self._current_interaction = self._initial_interaction()
        else:
            if self._current_interaction.answer is not None:
                self._current_interaction = self._closure_interaction(self._current_interaction.answer)
                if self._current_interaction.answer == TreasurePlay._CHOICE_LOOT:
                    self._parent.loot()

        return self._current_interaction
    
    def _initial_interaction(self):
        context, loot_choice, leave_choice = play_generation.generate_context(str(self._parent.intuitions))
        self._choices = {TreasurePlay._CHOICE_LOOT: loot_choice,
                         TreasurePlay._CHOICE_LEAVE: leave_choice}
        return Interaction(self, context, self._choices)

    def _closure_interaction(self, answer: int):
        loot = TreasurePlay._LEAVING_LOOT_TEXT if answer == TreasurePlay._CHOICE_LEAVE else self._parent.possible_loot
        closure = play_generation.generate_closure(self._current_interaction.query, self._choices[answer], loot)
        return Interaction(self, closure, None)

class LootedTreasurePlay(TreasurePlay):
    _ALREADY_LOOTED_LOOT_TEXT = "Nothing, because there is only one chest and it has already been looted"

    def __init__(self, parent):
        super().__init__(parent)

    def _initial_interaction(self):
        context, loot_choice, leave_choice = play_generation.generate_looted_context(str(self._parent.intuitions))
        self._choices = {TreasurePlay._CHOICE_LOOT: loot_choice,
                         TreasurePlay._CHOICE_LEAVE: leave_choice}
        return Interaction(self, context, self._choices)

    def _closure_interaction(self, answer: int):
        loot = LootedTreasurePlay._ALREADY_LOOTED_LOOT_TEXT if answer == TreasurePlay._CHOICE_LEAVE else TreasurePlay._LEAVING_LOOT_TEXT
        closure = play_generation.generate_closure(self._current_interaction.query, self._choices[answer], loot)
        return Interaction(self, closure, None)

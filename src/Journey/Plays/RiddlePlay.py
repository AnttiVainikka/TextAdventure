from typing import TYPE_CHECKING

from Generation.area import Area
from Generation.riddle_scene import *

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction
from Journey.utility import to_dict
from Journey.Action import (
    RiddleWrongAnswerAction,
    RiddleGoodAnswerAction,
    InteractionAnsweredAction
)

if TYPE_CHECKING:
    from Journey.Scenes.RiddleScene import RiddleScene

class RiddlePlay(Play):
    _INDEX_CONTEXT = 0
    _INDEX_RIDDLE = 1
    _INDEX_GOOD_ANSWER = 2
    _INDEX_WRONG_ANSWERS = [3, 4, 5]

    def __init__(self, parent: "RiddleScene", region_name: str, region_description: str, area: Area, difficulty: str):
        super().__init__(parent)
        self._current_wrong_answer_index = 0
        self._good_answer_given = False

        context = generate_intro_context(region_name, region_description, area.name, area.description)
        # The answer will be needed later on
        riddle, self._riddle_answer = generate_riddle(area.name, context, difficulty)
        good_answer = generate_good_answer_context(area.name,
                                                   context,
                                                   riddle,
                                                   self._riddle_answer)
        wrong_answers = [generate_wrong_answer_context(area.name, context, riddle, self._riddle_answer) for _ in range(3)]

        self._interactions.append(Interaction(self, context, True))
        self._interactions.append(Interaction(self, riddle))
        self._interactions.append(Interaction(self, good_answer, True))
        self._interactions.append(Interaction(self, wrong_answers[0], True))
        self._interactions.append(Interaction(self, wrong_answers[1], True))
        self._interactions.append(Interaction(self, wrong_answers[2], True))

    def __init_from_dict__(self, parent: "RiddleScene", state: dict):
        super().__init_from_dict__(parent, state)
        self._current_wrong_answer_index = state["current_wrong_answer_index"]
        self._good_answer_given = state["good_answer_given"]
        self._riddle_answer = state["riddle_answer"]

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["current_wrong_answer_index"] = to_dict(self._current_wrong_answer_index)
        state["good_answer_given"] = to_dict(self._good_answer_given)
        state["riddle_answer"] = to_dict(self._riddle_answer)
        return state

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interaction_riddle:
            self._good_answer_given = self._check_answer()
            if self._good_answer_given:
                self._raise_action(RiddleGoodAnswerAction(self))
            else:
                self._raise_action(RiddleWrongAnswerAction(self))

    @property
    def _interaction_context(self) -> "Interaction":
        return self._interactions[RiddlePlay._INDEX_CONTEXT]

    @property
    def _interaction_riddle(self) -> "Interaction":
        return self._interactions[RiddlePlay._INDEX_RIDDLE]
    
    @property
    def _interaction_good_answer(self) -> "Interaction":
        return self._interactions[RiddlePlay._INDEX_GOOD_ANSWER]
    
    @property
    def _interaction_wrong_answer(self) -> "Interaction":
        current = self._current_wrong_answer_index
        self._current_wrong_answer_index += 1
        self._current_wrong_answer_index %= len(RiddlePlay._INDEX_WRONG_ANSWERS)
        return self._interactions[RiddlePlay._INDEX_WRONG_ANSWERS[current]]
    
    @property
    def _wrong_interactions(self) -> "list[Interaction]":
        return self._interactions[RiddlePlay._INDEX_WRONG_ANSWERS[0]:RiddlePlay._INDEX_WRONG_ANSWERS[-1] + 1]

    def _next(self) -> Interaction:
        match self._current_interaction:
            case None:
                return self._interaction_context
            
            case self._interaction_context:
                return self._interaction_riddle
            
            case self._interaction_riddle:
                if self._good_answer_given:
                    return self._interaction_good_answer
                else:
                    return self._interaction_wrong_answer
                
            case self._interaction_good_answer:
                return self._interaction_good_answer
            
            case self._current_interaction if self._current_interaction in self._wrong_interactions:
                self._interaction_riddle.start()
                return self._interaction_riddle

    def _check_answer(self) -> bool:
        riddle_interaction = self._interactions[RiddlePlay._INDEX_RIDDLE]
        if riddle_interaction.is_answered:
            return check_answer(riddle_interaction.query,
                                self._riddle_answer,
                                riddle_interaction.answer)
        return False
    
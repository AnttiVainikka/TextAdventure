from typing import TYPE_CHECKING

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import ActionConcern, InteractionAnsweredAction
from Journey.utility import to_dict

if TYPE_CHECKING:
    from Journey.Plays.Play import Play

class UnknownAnswer(Exception):
    def __init__(self):
        super().__init__("Unknown answer")

class AlreadyAnswered(Exception):
    def __init__(self):
        super().__init__("Interaction has already been answered")

class Interaction(BaseActionComponent):
    """
    The Interaction class serves as a fundamental question-answer interface facilitating communication between a player and a Play.
    Its core functionality revolves around two essential methods:
        - The __str__ method is employed to prompt a question.
        - The __call__ method can be used to answer the question. This method also generates and returns the subsequent Interaction linked to the given answer.
    """
    def __init__(self, parent: "Play", query: str = "", is_info: bool = False):
        """
        Initializes an instance of the Interaction class.

        Parameters:
        - parent (Play): The Play object to which this interaction belongs.
        - query (str, optional): The question or state that needs to be answered. Defaults to an empty string.
        - is_info (bool, optional): Is this the closure for the interaction?
        """
        super().__init__(parent, ActionConcern.Interaction)
        self._query = query
        self._given_answer = None
        self._is_info = is_info

    def __init_from_dict__(self, parent: "Play", state: dict):
        super().__init__(parent, ActionConcern.Interaction)
        self._query = state["query"]
        self._given_answer = state["given_answer"]
        self._is_info = state["is_info"]

    def create_from_dict(parent: "Play", state: dict) -> "Interaction":
        if state is None: return None

        interaction_cls = globals()[state["type"]]
        if interaction_cls is not None:
            interaction = interaction_cls.__new__(interaction_cls)
            interaction.__init_from_dict__(parent, state)
            return interaction
        return None

    def to_dict(self) -> dict:
        return {
            "type": to_dict(type(self).__name__),
            "query": to_dict(self._query),
            "given_answer": to_dict(self._given_answer),
            "is_info": to_dict(self._is_info)
        }

    @property
    def is_answered(self) -> bool:
        return self._given_answer != None

    @property
    def answer(self) -> object | None:
        """
        Retrieves the answer if the question has been answered. If the question remains unanswered,
        it returns None.

        Returns:
        - object or None: An object representing the answer if the question has been answered, 
          or None if the question is unanswered.
        """
        return self._given_answer

    @property
    def query(self) -> str:
        """
        Retrieves the query text associated with the Interaction.

        Returns:
        - str: The query text linked to the Interaction.
        """
        return self._query

    @property
    def is_info(self) -> bool:
        """
        Checks if the Interaction instance represents the final interaction with the player.

        Returns:
        - bool: True if the Interaction is the last interaction with the player; False otherwise.
        """
        return self._is_info

    def restart(self):
        self._given_answer = None

    def __call__(self, answer: object):
        """
        This can be used to answer the question within of the Interaction class. 

        If this insance is a closure, UnexpectedAnswer exception is raised.
        
        Parameters:
        - answer (object): The answer intended to respond to the question.

        Raises:
        - UnexpectedAnswer: If this instance is a closure.
        """
        if not self._is_info and self._given_answer is not None:
            raise AlreadyAnswered()
        
        # If this is just an information interaction then the given answer is not important
        if self._is_info:
            self._given_answer = ""
        else:
            self._given_answer = answer
        self._raise_action(InteractionAnsweredAction(self))

    def __str__(self) -> str:
        """
        This method customizes the string representation of the Interaction class instance.
        This can be used to prompt the Interaction to the user.

        Returns:
        - str: A string containing the question and possible answers to prompt the user.
        """
        return self._query

class QSAInteraction(Interaction):
    """
    The QSAInteraction class serves as a fundamental question-answer interface facilitating communication between a player and a Play,
    where the player can choose between pregenerated answers.
    Its core functionality revolves around two essential methods:
        - The __str__ method is employed to prompt a question, presenting the available answer choices.
        - The __call__ method can be used to answer the question. This method also generates and returns the subsequent QSAInteraction linked to the given answer.
    """
    def __init__(self, parent: "Play", query: str = "", possible_answers: dict[int, str] = {}):
        """
        Initializes an instance of the QSAInteraction class.

        Parameters:
        - parent (Play): The Play object to which this interaction belongs.
        - query (str, optional): The question or state that needs to be answered. Defaults to an empty string.
        - possible_answers (dict[int, str], optional): A dictionary of possible answers. 
          The keys represent identifiers for answers, and the values are the answers in string form.
        """
        super().__init__(parent, query, possible_answers is None or len(possible_answers) == 0)
        self._possible_answers = possible_answers

    def __init_from_dict__(self, parent: "Play", state: dict):
        super().__init_from_dict__(parent, state)
        self._possible_answers = {int(key): value for key, value in state["possible_answers"].items()}

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["possible_answers"] = self._possible_answers
        return state

    @property
    def possible_answers(self) -> dict:
        return self._possible_answers

    def key_to_answer(self, key: int):
        return self._possible_answers[key]

    def answer_to_key(self, answer: str):
        for key, value in self._possible_answers.items():
            if value == answer:
                return key
        return None

    def remove_answer(self, key: int):
        if key in self._possible_answers:
            del self._possible_answers[key]
        
        new_possible_answers = {}
        new_key = min(self._possible_answers.keys())
        for key, value in sorted(self._possible_answers.items()):
            new_possible_answers[new_key] = value
            new_key += 1
        self._possible_answers = new_possible_answers

    def __call__(self, answer: int):
        """
        This can be used to answer the question within of the QSAInteraction class. 

        If the provided 'answer' is one of the predefined answers, it returns the follow-up question.
        If the 'answer' is not provided in the predefined answers, it raises an exception.

        Parameters:
        - answer (int): The answer key intended to respond to the question.

        Raises:
        - UnknownAnswer: If the provided answer is not one of the predefined answers.
        """
        answer = int(answer)
        if answer not in self._possible_answers:
            raise UnknownAnswer()
        super().__call__(answer)
        
    def __str__(self) -> str:
        """
        This method customizes the string representation of the QSAInteraction class instance.
        This can be used to prompt the QSAInteraction to the user.
        It prompts the question and displays the possible answers.

        Returns:
        - str: A string containing the question and possible answers to prompt the user.
        """
        s = super().__str__()
        if not self._is_info:
            s += f"\n{self._AnswersFormat()}"
        return s

    def _AnswersFormat(self) -> str:
        form = ""
        for key, value in self._possible_answers.items():
            form += f"\n{key} - {value}"
        return form
    
    

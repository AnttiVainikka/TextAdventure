from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Journey.Play import Play

class UnknownAnswer(Exception):
    def __init__(self):
        super().__init__("Unknown answer")

class UnexpectedAnswer(Exception):
    def __init__(self):
        super().__init__("Unexpected answer for a closure")

class Interaction:
    """
    The Interaction class serves as a fundamental question-answer interface facilitating communication between a player and a Play.
    Its core functionality revolves around two essential methods:
        - The __str__ method is employed to prompt a question.
        - The __call__ method can be used to answer the question. This method also generates and returns the subsequent Interaction linked to the given answer.
    """
    def __init__(self, parent: "Play", query: str = "", is_closure: bool = False):
        """
        Initializes an instance of the Interaction class.

        Parameters:
        - parent (Play): The Play object to which this interaction belongs.
        - query (str, optional): The question or state that needs to be answered. Defaults to an empty string.
        - is_closure (bool, optional): Is this the closure for the interaction?
        """
        self._parent = parent
        self._query = query
        self._given_answer = None
        self._is_closure = is_closure

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
    def is_closure(self) -> bool:
        """
        Checks if the Interaction instance represents the final interaction with the player.

        Returns:
        - bool: True if the Interaction is the last interaction with the player; False otherwise.
        """
        return self._is_closure

    def __call__(self, answer: object) -> "Interaction":
        """
        This can be used to answer the question within of the Interaction class. 

        If this insance is a closure, UnexpectedAnswer exception is raised.
        
        Parameters:
        - answer (object): The answer intended to respond to the question.

        Raises:
        - UnexpectedAnswer: If this instance is a closure.
        """
        if self._is_closure:
            raise UnexpectedAnswer()
        self._given_answer = answer
        return self._parent.interact

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
        super().__init__(parent, query, len(possible_answers) > 0)
        self._possible_answers = possible_answers

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
        if answer not in self._possible_answers:
            raise UnknownAnswer()
        return super().__call__(answer)
        
    def __str__(self) -> str:
        """
        This method customizes the string representation of the QSAInteraction class instance.
        This can be used to prompt the QSAInteraction to the user.
        It prompts the question and displays the possible answers.

        Returns:
        - str: A string containing the question and possible answers to prompt the user.
        """
        s = super().__str__()
        if not self._is_closure:
            s += f"\n{self._AnswersFormat()}"
        return s

    def _AnswersFormat(self) -> str:
        form = ""
        for key, value in self._possible_answers.items():
            form += f"\n{key} - {value}"
        return form

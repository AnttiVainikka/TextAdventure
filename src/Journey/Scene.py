from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Journey.Intuition import Intuitions
    from Journey.Play import Play
    from Journey.Layout import Layout, Difficulty

class Scene(ABC):
    """
    A Scene serves as a fundamental element within the Layout, representing an intresting part or significant event within the Layout.

    Scenes are comprised of Plays, the interactions between the player and the Scene, generated based on Intuitions.

    Each Scene maintains its own history, capturing essential information about the occurrences within.
    When a Scene is finished, these records are converted into Intuitions and spread to subsequent Scenes.
    This mechanism enriches the connections and coherence between Scenes within the Layout.
    """
    def __init__(self, parent: "Layout", difficulty: "Difficulty", intuitions: "Intuitions"):
        """
        Constructor for the Scene class.

        Parameters:
        - parent (Layout): The parent layout to which the Scene belongs.
        - difficulty (Difficulty): Difficulty level of the Scene.
        - intuitions (Intuitions): The intuitions based on which the Scene will be generated.
        """
        self._parent = parent
        self._difficulty = difficulty
        self._intuitions = intuitions
        self._history = []
        self._plays = []

    @property
    def intuitions(self) -> "Intuitions":
        """
        Retrieve the intuitions based on which the Scene was generated.

        Returns:
        - Intuitions: The intuitions that were used to generate the Scene.
        """
        return self._intuitions

    @property
    def difficulty(self) -> "Difficulty":
        """
        Retrieve the difficulty level of the Scene.

        Returns:
        - Difficulty: The difficulty level of the Scene.
        """
        return self._difficulty

    @property
    def history(self) -> list[str]:
        """
        Retrieve the history of the Scene.

        Returns:
        - list[str]: The history of the Scene.
        """
        return self._history

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check whether the current scene has been completed.

        Returns:
        - bool: Returns True if the current scene has been completed; otherwise, returns False.
        """
        pass

    @abstractmethod
    def play(self) -> "Play":
        """
        Retrieve the currently active play of the Scene.

        Returns:
        - Play: The currently active play of the Scene.
        """
        pass

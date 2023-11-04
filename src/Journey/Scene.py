from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Journey.Circumstance import Circumstances
    from Journey.Play import Play
    from Journey.Layout import Layout, Difficulty

class Scene(ABC):
    """
    A Scene serves as a fundamental element within the Layout, representing an intresting part or significant event within the Layout.

    Scenes are comprised of Plays, the interactions between the player and the Scene, generated based on Circumstances.

    Each Scene maintains its own history, capturing essential information about the occurrences within.
    When a Scene is finished, these records are converted into Circumstances and spread to subsequent Scenes.
    This mechanism enriches the connections and coherence between Scenes within the Layout.
    """
    def __init__(self, parent: "Layout", difficulty: "Difficulty", circumstances: "Circumstances"):
        """
        Constructor for the Scene class.

        Parameters:
        - parent (Layout): The parent layout to which the Scene belongs.
        - difficulty (Difficulty): Difficulty level of the Scene.
        - circumstances (Circumstances): The circumstances based on which the Scene will be generated.
        """
        self._parent = parent
        self._difficulty = difficulty
        self._intuitions = circumstances
        self._history = []
        self._plays = []

    @property
    def circumstances(self) -> "Circumstances":
        """
        Retrieve the circumstances based on which the Scene was generated.

        Returns:
        - Circumstances: The circumstances that were used to generate the Scene.
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

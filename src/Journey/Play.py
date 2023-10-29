from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Journey.Interaction import Interaction
    from Journey.Scene import Scene

class Play(ABC):
    """
    Play represents the interaction between the player and a Scene.

    Interactions are generated based on Intuitions and facilitated through Interaction objects.
    """
    def __init__(self, parent: "Scene"):
        """
        Constructor for the Play class.

        Parameters:
        - parent (Scene): The parent Scene to which the Play belongs.
        """
        self._parent = parent

    @property
    def interact(self) -> "Interaction":
        """
        Generate and return the Interaction object based on the status of the Play.

        Returns:
        - Interaction: Returns the Interaction object representing the interaction with the Play.
        """
        return self._generate_next_interaction()

    @abstractmethod
    def _generate_next_interaction(self) -> "Interaction":
        pass

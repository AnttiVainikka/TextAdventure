from typing import TYPE_CHECKING

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction

from Journey.Action import InteractionAnsweredAction, PlayFinishedAction

if TYPE_CHECKING:
    from Journey.Scenes.CapitalScene import CapitalScene

class FactionPlay(Play):
    # TODO: Not sure what faction is or what other objects you need
    def __init__(self, parent: "CapitalScene", faction: object):
        super().__init__(parent)
        # TODO: Maybe a welcome message/context or something. Not necessary
        self._interactions.append(Interaction(self, "You are at the quartel of faction Uvuvwevwevwe", True))
        self._faction = faction
        # TODO: Maybe a history should also be created to maintain

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._current_interaction and interaction.is_answered:
            self._interactions.append(self._get_next_interaction(interaction))

    def has_next(self):
        return self._interactions[-1] is not None and not self._interactions[-1].is_answered

    def reset(self):
        super().reset()
        self._interactions = self._interactions[0]

    def _next(self) -> Interaction:
        match self._current_interaction:
            case None:
                return self._interactions[0]
            
            case _:
                return self._interactions[-1]
            
    def _get_next_interaction(self, interaction: Interaction) -> Interaction:
        # TODO:

        # Process the answer and generate a new Interaction

        # Interaction contains both the "question" and the answer
        
        # Based on those I assume it is possible to generate the next interaction. Or if you already have some other object that maintains this,
        # you probably need just the answer

        # If there is nothing else to say return None

        # If something special happens that cannot be handled here, for example the player receives an item, or the faction joins 
        # you can raise an action which is basicly an easier parent.parent.parent.parent... call
        # self._raise_action(ActionName())
        # All you have to do is define the Action in Journey.Actions and handle it in its destination "def _process_ActionName(self, action: ActionName)"
        if interaction == self._interactions[0]:
            return Interaction(self, "Kuka sinä olet?") # Just to show off my very serious Finnish skills
        
        if interaction.query == "Kuka sinä olet?":
            name = interaction.answer
            return Interaction(self, f"Tervetuloa {name}!", True) # If you set this to True, no answer is expected
        elif interaction.query.startswith("Tervetuloa"):
            return Interaction(self, f"Mitä kuulu?")
        elif interaction.query == "Mitä kuulu?":
            return Interaction(self, f"En välitä.", True)
        else:
            self._raise_action(PlayFinishedAction(self))
            return None
        
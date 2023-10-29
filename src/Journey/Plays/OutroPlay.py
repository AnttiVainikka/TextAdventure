from typing import TYPE_CHECKING
from Generation.outro_scene import generate

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction
from Journey.Action import InteractionAnsweredAction, PlayFinishedAction

if TYPE_CHECKING:
    from Journey.Scenes.OutroScene import OutroScene

class OutroPlay(Play):
    def __init__(self, parent: "OutroScene", region_name: str, capital_name: str, mission: str):
        super().__init__(parent)
        context = generate(region_name, mission, capital_name)
        self._interactions.append(Interaction(self, context, True))

    def _process_InteractionAnswered(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[0]:
            self._raise_action(PlayFinishedAction(self))

    def has_next(self) -> bool:
        return self._current_interaction != self._interactions[0]

    def _next(self) -> Interaction:
        return self._interactions[0]

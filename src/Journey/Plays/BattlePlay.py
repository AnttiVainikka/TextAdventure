from typing import TYPE_CHECKING

from Generation.area import Area
from Generation.battle_scene import *

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction
from Journey.Action import InteractionAnsweredAction, PlayFinishedAction, StartBattleAction

if TYPE_CHECKING:
    from Journey.Scenes.BattleScene import BattleScene

class BattlePlay(Play):
    _INDEX_INTRO = 0
    _INDEX_OUTRO = 1

    def __init__(self, parent: "BattleScene", region_name: str,
                                              region_description: str,
                                              area: Area,
                                              enemy_types: list[EnemyType],
                                              leader: EnemyType = None):
        super().__init__(parent)
        intro_context = generate_intro_context(region_name,
                                               region_description,
                                               area.name,
                                               area.description,
                                               enemy_types,
                                               leader)
        
        outro_context = generate_outro_context(region_name,
                                               region_description,
                                               area.name,
                                               area.description,
                                               enemy_types,
                                               leader)
        
        self._interactions.append(Interaction(self, intro_context, True))
        self._interactions.append(Interaction(self, outro_context, True))

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        interaction = action.interaction
        if interaction == self._interactions[BattlePlay._INDEX_INTRO]:
            self._raise_action(StartBattleAction(self))
        elif interaction == self._interactions[BattlePlay._INDEX_OUTRO]:
            self._raise_action(PlayFinishedAction(self))

    def _next(self) -> Interaction:
        if self._current_interaction == self._interactions[BattlePlay._INDEX_INTRO]:
            return self._interactions[BattlePlay._INDEX_OUTRO]
        else:
            return self._interactions[BattlePlay._INDEX_INTRO]

from typing import TYPE_CHECKING

from Generation.area import Area
from Generation.final_battle_scene import *
from Generation.enemy_type import EnemyType

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction
from Journey.Action import InteractionAnsweredAction

if TYPE_CHECKING:
    from Journey.Scenes.FinalBattleScene import FinalBattleScene

class FinalBattlePlay(Play):
    _INDEX_INTRO_P1 = 0
    _INDEX_OUTRO_P1 = 1
    _INDEX_INTRO_P2 = 2
    _INDEX_OUTRO_P2 = 3

    def __init__(self, parent: "FinalBattleScene", region_name: str, mission_quest: str, area: Area, boss: EnemyType):
        super().__init__(parent)
        intro_context = generate_intro(region_name, area.name, area.description, mission_quest, boss.name)
        outro_context = generate_outro(region_name, area.name, intro_context, mission_quest, boss.name)
        intro_context_p2 = generate_intro_p2(region_name, area.name, intro_context + outro_context,
                                                   mission_quest, boss.name)
        outro_context_p2 = generate_outro_p2(region_name, area.name, intro_context + outro_context + intro_context_p2,
                                                   mission_quest, boss.name)

        self._interactions.append(Interaction(self, intro_context, True))
        self._interactions.append(Interaction(self, outro_context, True))
        self._interactions.append(Interaction(self, intro_context_p2, True))
        self._interactions.append(Interaction(self, outro_context_p2, True))

    def _process_InteractionAnsweredAction(self, action: InteractionAnsweredAction):
        pass

    @property
    def _interaction_intro_p1(self) -> "Interaction":
        return self._interactions[FinalBattlePlay._INDEX_INTRO_P1]

    @property
    def _interaction_outro_p1(self) -> "Interaction":
        return self._interactions[FinalBattlePlay._INDEX_OUTRO_P1]
    
    @property
    def _interaction_intro_p2(self) -> "Interaction":
        return self._interactions[FinalBattlePlay._INDEX_INTRO_P2]
    
    @property
    def _interaction_outro_p2(self) -> "Interaction":
        return self._interactions[FinalBattlePlay._INDEX_OUTRO_P2]

    def has_next(self) -> bool:
        return self._current_interaction != self._interaction_outro_p2

    def _next(self, ) -> Interaction:
        match self._current_interaction:
            case None:
                return self._interaction_intro_p1
            case self._interaction_intro_p1:
                return self._interaction_outro_p1
            case self._interaction_outro_p1:
                return self._interaction_intro_p2
            case self._interaction_intro_p2:
                return self._interaction_outro_p2
            case _:
                return self._current_interaction
                
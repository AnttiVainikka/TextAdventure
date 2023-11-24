from typing import TYPE_CHECKING
from Characters.character import Character

from Generation.area import Area
from Generation.scenario import Scenario
from Journey.Difficulty import Difficulty

from Journey.Layout import Layout
from Journey.Mission import Mission
from Journey.Scenes.IntroScene import IntroScene
from Journey.Scenes.OutroScene import OutroScene
from Journey.Scenes.FinalBattleScene import FinalBattleScene
from llm import complete

if TYPE_CHECKING:
    from Journey.Journey import Journey

class SiegeLayout(Layout):
    def __init__(self,
                 parent: "Journey",
                 name: str,
                 description: str,
                 number_of_areas: int):
        super().__init__(parent, name, description, number_of_areas)

    def _create_mission(self) -> Mission:
        player: Character = self.parent.character
        scenario: Scenario = self.parent.scenario
        base_prompt = f"""You are an AI text adventure game master.
---
The game takes place in capital city {scenario.capital.name} of the medieval fantasy kingdom {scenario.kingdom.name}. The kingdom is ruled by {scenario.ruler.name}. {scenario.ruler.personality} {scenario.ruler.evil_deeds} {scenario.ruler.governance_style}

A rebellion has been brewing for a long time. Now, the time is right. The rebel leader {player.name} is launching an attack to the ruler's castle.

The attack takes place in center of the capital city. Here is its description:
{scenario.capital.architecture} {scenario.capital.history}"""
        
        for faction in player.allies:
            prompt = f"""{base_prompt}

The rebel leader has brought their ally, {faction.name}, to help. {faction.overview} {faction.beliefs} {faction.goals} {faction.name} is {faction.alignment.value}.

Write a short description about how {faction.name} will help the rebel leader:
"""
            result = complete(prompt)
            print(result)
        return Mission(description='', quest_description='', objective='')

    def _create_intro_scene(self) -> IntroScene:
        return IntroScene(self)

    def _create_last_scene(self, area: Area) -> FinalBattleScene:
        return FinalBattleScene(self, area, Difficulty.Challenging)
    
    def _create_outro_scene(self) -> OutroScene:
        return OutroScene(self)

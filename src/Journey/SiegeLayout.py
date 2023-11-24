from typing import TYPE_CHECKING

from Generation.area import Area

from Journey.Layout import Layout
from Journey.Mission import Mission
from Journey.Scenes.IntroScene import IntroScene
from Journey.Scenes.OutroScene import OutroScene
from Journey.Scenes.FinalBattleScene import FinalBattleScene

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
        pass

    def _create_intro_scene(self) -> IntroScene:
        pass

    def _create_last_scene(self, area: Area) -> FinalBattleScene:
        pass
    
    def _create_outro_scene(self) -> OutroScene:
        pass

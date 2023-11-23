from typing import TYPE_CHECKING
import time

from Journey.BaseLayout import BaseLayout
from Journey.BaseActionComponent import BaseActionComponent, ActionConcern
from Journey.Scenes.CapitalScene import CapitalScene
from Journey.Scenes.Scene import Scene
from Journey.utility import to_dict
from Journey.LoopManager import LoopManager
from Journey.Scenes import create_from_dict as create_scene

if TYPE_CHECKING:
    from Journey.Journey import Journey

class CapitalLayout(BaseLayout):
    def __init__(self, parent: "Journey"):
        super().__init__(parent)
        kingdom = parent.kingdom
        self._scenes.append(CapitalScene(self, parent.factions, [region.name for region in kingdom.regions]))

    @property
    def scene(self) -> CapitalScene:
        return self._scenes[0]

    def remove_region(self, region: str):
        self.scene.remove_region(region)

    def create_from_dict(parent: "Journey", state: dict) -> "BaseLayout":
        layout = CapitalLayout.__new__(CapitalLayout)
        layout.__init_from_dict__(parent, state)
        return layout

    def _first_scene(self) -> CapitalScene:
        return self._scenes[0]

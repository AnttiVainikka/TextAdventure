from typing import TYPE_CHECKING
from random import randint

from abc import ABC, abstractmethod

from Journey.Scenes.Scene import Scene
from Journey.Scenes import create_from_dict as create_scene
from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import *
from Journey.utility import to_dict, to_dict_index, from_dict_index
from Journey.LoopManager import LoopManager

if TYPE_CHECKING:
    from Journey.Journey import Journey

class BaseLayout(BaseActionComponent, LoopManager, ABC):
    def __init__(self, parent: "Journey"):
        BaseActionComponent.__init__(self, parent, ActionConcern.Layout)
        LoopManager.__init__(self)

        self._scenes = []
        self._current_scene = None

    def __init_from_dict__(self, parent: "Journey", state: dict):
        BaseActionComponent.__init__(self, parent, ActionConcern.Layout)
        LoopManager.__init__(self)
        self._scenes = [create_scene(self, scene_dict) for scene_dict in state["scenes"]]
        self._current_scene = from_dict_index(state, "current_scene", self._scenes)
        
    def to_dict(self) -> dict:
        return {
            "scenes": to_dict(self._scenes),
            "current_scene": to_dict_index(self._current_scene, self._scenes)
        }
    
    @abstractmethod
    def _first_scene(self) -> Scene:
        pass

    def next(self) -> Scene:
        if self._current_scene is None:
            self._current_scene = self._first_scene()
        return self._current_scene
    
    def _do_work(self):
        scene = self.next()
        scene.run()

    def stop(self):
        self._current_scene.stop()
        super().stop()

from typing import TYPE_CHECKING
from random import randint

from Generation.area import Area, generate as generate_areas
from Generation.scenario import Kingdom
from Generation.selection import Selector, NonRepSelector

from Journey.Scenes.Scene import Scene
from Journey.Scenes import create_from_dict as create_scene
from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import *
from Journey.Mission import Mission, ArtifactMission, TargetMission
from Journey.utility import to_dict
from Journey.Difficulty import Difficulty

from Journey.Scenes.IntroScene import IntroScene
from Journey.Scenes.RiddleScene import RiddleScene
from Journey.Scenes.TreasureScene import TreasureScene
from Journey.Scenes.RestScene import RestScene
from Journey.Scenes.BattleScene import BattleScene
from Journey.Scenes.FinalBattleScene import FinalBattleScene
from Journey.Scenes.OutroScene import OutroScene

if TYPE_CHECKING:
    from Journey.Journey import Journey

import log

_logger = log.getLogger(__name__)

class Layout(BaseActionComponent):
    _DIFFICULTY_PROBABILITIES = {
        Difficulty.Easy: 0.35,
        Difficulty.Normal: 0.35,
        Difficulty.Hard: 0.2,
        Difficulty.Challenging: 0.1
    }

    _SCENE_PROBABILITIES = {
        TreasureScene: 0.15,
        BattleScene: 0.5,
        RiddleScene: 0.35
    }

    _SCENE_SELECTOR_LAMBDA = 0.5

    _MISSION_CLASSES = [ArtifactMission, TargetMission]

    def __init__(self,
                 parent: "Journey",
                 name: str,
                 description: str,
                 number_of_areas: int):
        super().__init__(parent, ActionConcern.Layout)

        self._name = name
        self._description = description

        kingdom: Kingdom = self._parent.kingdom
        # Creating mission
        _logger.info(f"Creating mission for layout {self._name}")
        self._mission: Mission = Layout._MISSION_CLASSES[randint(0, len(Layout._MISSION_CLASSES) - 1)].generate(kingdom.name, kingdom.description, self._name)
        _logger.debug(f"Mission created: {self._mission.to_dict()}")

        # Creating areas
        _logger.info(f"Creating areas for layout {self._name}")
        self._areas = generate_areas(kingdom.name, self._name, self._description, self._mission.quest_description, number_of_areas)
        _logger.debug(f"Areas created:")
        for (i, area) in enumerate(self._areas):
            _logger.debug(f"{i + 1}: {area.name} - {area.description}")

        # Creating scenes
        self._scenes: list[Scene] = []
        difficulty_selector = Selector(list(Layout._DIFFICULTY_PROBABILITIES.keys()), list(Layout._DIFFICULTY_PROBABILITIES.values()))
        scene_selector = NonRepSelector(list(Layout._SCENE_PROBABILITIES.keys()),
                                        list(Layout._SCENE_PROBABILITIES.values()),
                                             Layout._SCENE_SELECTOR_LAMBDA)

        _logger.info(f"Creating intro scene for layout {self._name}")
        self._scenes.append(IntroScene(self, area, Difficulty.Easy))

        # The last 3 scenes are : rest -> battle -> battle
        for area in self._areas[:-3]:
            scene_class = scene_selector()
            difficulty = difficulty_selector()

            _logger.info(f"Creating {scene_class.__name__} for layout {self._name}")
            self._scenes.append(scene_class(self, area, difficulty))

        _logger.info(f"Creating {RestScene.__name__} for layout {self._name}")
        self._scenes.append(RestScene(self, self._areas[-3], Difficulty.Easy))

        _logger.info(f"Creating {BattleScene.__name__} for layout{self._name}")
        self._scenes.append(BattleScene(self, self._areas[-2], Difficulty.Hard))

        _logger.info(f"Creating {FinalBattleScene.__name__} for layout{self._name}")
        self._scenes.append(FinalBattleScene(self, self._areas[-1], Difficulty.Challenging))

        _logger.info(f"Creating {OutroScene.__name__} for layout {self._name}")
        self._scenes.append(OutroScene(self))

        self._nr_finished_scenes = 0

    def __init_from_dict__(self, parent: "Journey", state: dict):
        super().__init__(parent, ActionConcern.Layout)
        self._name = state["name"]
        self._description = state["description"]
        self._mission = Mission.create_from_dict(state["mission"])
        self._areas = [Area(area["name"], area["description"]) for area in state["areas"]]
        self._scenes = [create_scene(self, scene_dict) for scene_dict in state["scenes"]]

    def create_from_dict(parent: "Journey", state: dict) -> "Layout":
        layout = Layout.__new__(Layout)
        layout.__init_from_dict__(parent, state)
        return layout

    def to_dict(self) -> dict:
        return {
            "name": to_dict(self._name),
            "description": to_dict(self._description),
            "mission": to_dict(self._mission),
            "areas": [to_dict(area) for area in self._areas],
            "scenes": [to_dict(scene) for scene in self._scenes]
        }
    
    def has_next(self) -> bool:
        return self.current_scene != self.scenes[-1] or\
               not self.current_scene.is_finished

    def next(self) -> Scene:
        return self.current_scene

    ############
    # Properties
    @property
    def is_finished(self) -> bool:
        return self._nr_finished_scenes == len(self._scenes)

    @property
    def number_of_finished_scenes(self) -> int:
        return self._nr_finished_scenes

    @property
    def current_scene(self) -> Scene:
        if self._nr_finished_scenes >= len(self._scenes): return self._scenes[-1]
        return self._scenes[self._nr_finished_scenes]

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description

    @property
    def areas(self) -> list[Area]:
        return self._areas

    @property
    def scenes(self) -> list[Scene]:
        return self._scenes

    @property
    def mission(self) -> Mission:
        return self._mission

    @property
    def capital(self) -> str:
        return self._parent.capital
    
    ############
    # Processes
    def _process_SceneFinishedAction(self, action: SceneFinishedAction):
        scene = action.scene
        if self._nr_finished_scenes == len(self._scenes): return
        if scene == self.current_scene and scene.is_finished:
            self._nr_finished_scenes += 1
            if self._nr_finished_scenes == len(self._scenes):
                self._raise_action(LayoutFinishedAction(self))
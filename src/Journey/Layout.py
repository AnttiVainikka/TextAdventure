from typing import TYPE_CHECKING
from random import randint

from Generation.area import Area, generate as generate_areas
from Generation.scenario import Kingdom
from Generation.selection import Selector, NonRepSelector

from Journey.Scenes.Scene import Scene
from Journey.Scenes import create_from_dict as create_scene
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

from Journey.BaseLayout import BaseLayout

if TYPE_CHECKING:
    from Journey.Journey import Journey

import log

_logger = log.getLogger(__name__)

class Layout(BaseLayout):
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
        super().__init__(parent)

        self._name = name
        self._description = description

        self._mission = self._create_mission()
        self._areas = self._create_areas(number_of_areas)
        self._scenes = [self._create_intro_scene()]
        self._scenes += self._create_random_scenes(self._areas[:-3])
        self._scenes.append(self._create_rest_scene(self._areas[-3]))
        self._scenes.append(self._create_second_last_scene(self._areas[-2]))
        self._scenes.append(self._create_last_scene(self._areas[-1]))
        self._scenes.append(self._create_outro_scene())

    def __init_from_dict__(self, parent: "Journey", state: dict):
        super().__init_from_dict__(parent, state)
        self._name = state["name"]
        self._description = state["description"]
        self._mission = Mission.create_from_dict(state["mission"])
        self._areas = [Area(area["name"], area["description"]) for area in state["areas"]]

    def create_from_dict(parent: "Journey", state: dict) -> "Layout":
        if state is None: return None
        layout = Layout.__new__(Layout)
        layout.__init_from_dict__(parent, state)
        return layout

    def to_dict(self) -> dict:
        return {
            "name": to_dict(self._name),
            "description": to_dict(self._description),
            "mission": to_dict(self._mission),
            "areas": [to_dict(area) for area in self._areas]
        }
    
    def _first_scene(self) -> "Scene":
        return self._scenes[0]

    ############
    # Properties
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
        if scene == self._current_scene:
            self._current_scene.stop()
            index = self._scenes.index(self._current_scene)
            if index < len(self._scenes) - 1:
                self._current_scene = self._scenes[index + 1]
            else:
                self.stop()
                self._raise_action(LayoutFinishedAction(self))

    def _process_EnterRegionAction(self, action: EnterRegionAction):
        self._current_scene = self.scenes[1]

    def _create_mission(self) -> Mission:
        _logger.info(f"Creating mission for layout {self._name}")
        
        kingdom: Kingdom = self._parent.kingdom
        mission = Layout._MISSION_CLASSES[randint(0, len(Layout._MISSION_CLASSES) - 1)].generate(kingdom.name, kingdom.description, self._name)
        
        _logger.debug(f"Mission created: {mission.to_dict()}")
        return mission
    
    def _create_areas(self, number_of_areas: int) -> list[Area]:
        _logger.info(f"Creating areas for layout {self._name}")

        kingdom: Kingdom = self._parent.kingdom
        areas = generate_areas(kingdom.name, self._name, self._description, self._mission.quest_description, number_of_areas)
        
        _logger.debug(f"Areas created:")
        for (i, area) in enumerate(areas):
            _logger.debug(f"{i + 1}: {area.name} - {area.description}")

        return areas
    
    def _create_intro_scene(self) -> IntroScene:
        _logger.info(f"Creating {IntroScene.__name__} for layout {self._name}")
        self._scenes.append(IntroScene(self, Difficulty.Easy))

    def _create_random_scenes(self, areas: list[Area]) -> list[Scene]:
        # Creating scenes
        difficulty_selector = Selector(list(Layout._DIFFICULTY_PROBABILITIES.keys()), list(Layout._DIFFICULTY_PROBABILITIES.values()))
        
        scene_selector = NonRepSelector(list(Layout._SCENE_PROBABILITIES.keys()),
                                        list(Layout._SCENE_PROBABILITIES.values()),
                                             Layout._SCENE_SELECTOR_LAMBDA)

        scenes = []
        for area in areas:
            scene_class = scene_selector()
            difficulty = difficulty_selector()

            _logger.info(f"Creating {scene_class.__name__} for layout {self._name}")
            scenes.append(scene_class(self, area, difficulty))

        return scenes

    def _create_rest_scene(self, area: Area) -> RestScene:
        _logger.info(f"Creating {RestScene.__name__} for layout {self._name}")
        return RestScene(self, area, Difficulty.Easy)
    
    def _create_second_last_scene(self, area: Area) -> BattleScene:
        _logger.info(f"Creating {BattleScene.__name__} (second last) for layout{self._name}")
        return BattleScene(self, area, Difficulty.Hard)

    def _create_last_scene(self, area: Area) -> FinalBattleScene:
        _logger.info(f"Creating {FinalBattleScene.__name__} for layout{self._name}")
        return FinalBattleScene(self, area, Difficulty.Challenging)
    
    def _create_outro_scene(self) -> OutroScene:
        _logger.info(f"Creating {OutroScene.__name__} for layout {self._name}")
        self._scenes.append(OutroScene(self))

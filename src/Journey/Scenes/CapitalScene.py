from typing import TYPE_CHECKING

from Generation.faction import Faction

from Journey.Scenes.Scene import Scene
from Journey.Difficulty import Difficulty

from Journey.Plays.Play import Play
from Journey.Plays.Capital.FactionPlay import FactionPlay
from Journey.Plays.SelectionPlay import SelectionPlay

from Journey.Action import *

if TYPE_CHECKING:
    from Journey.Layout import Layout

class CapitalScene(Scene):
    _INDEX_MAIN = 0
    _INDEX_FACTION_SELECTION = 1
    _INDEX_REGION_SELECTION = 2
    _INDEX_START_FACTIONS = 3
    
    class MainChoice(Enum):
        SELECT_REGION = 1
        SELECT_FACTION = 2

    _MAIN_QUESTION = "Where do you want to go?"
    _MAIN_CHOICES = {
        MainChoice.SELECT_REGION.value: "Select region...",
        MainChoice.SELECT_FACTION.value: "Select faction..."
    }

    _REGION_QUESTION = "Where do you want to go?"
    _FACTION_QUESTION = "Who do you want to talk to?"

    def __init__(self, parent: "Layout", factions: list[Faction], regions: list[str]):
        super().__init__(parent, None, Difficulty.Easy)
        self._plays.append(SelectionPlay(self, CapitalScene._MAIN_QUESTION, CapitalScene._MAIN_CHOICES))
        self._plays.append(SelectionPlay(self, CapitalScene._FACTION_QUESTION, [faction.name for faction in factions]))
        self._plays.append(SelectionPlay(self, CapitalScene._REGION_QUESTION, regions))
        for faction in factions:
            self._plays.append(FactionPlay(self, parent.parent.character, parent.parent.scenario, faction))
        self._current_play = self._play_main

    def remove_region(self, region: str):
        self._play_region_selection.remove(region)

    @property
    def _play_main(self) -> SelectionPlay:
        return self._plays[CapitalScene._INDEX_MAIN]

    @property
    def _play_faction_selection(self) -> SelectionPlay:
        return self._plays[CapitalScene._INDEX_FACTION_SELECTION]

    @property
    def _play_region_selection(self) -> SelectionPlay:
        return self._plays[CapitalScene._INDEX_REGION_SELECTION]

    @property
    def _play_faction(self) -> list[FactionPlay]:
        return self._plays[CapitalScene._INDEX_START_FACTIONS:]

    def _process_SelectionAction(self, action: SelectionAction):
        play = action.play
        if play == self._current_play:
            self._current_play.stop()
            match play:
                case self._play_main:
                    self._process_main_selection(action.index)

                case self._play_region_selection:
                    self._process_region_selection(action.index, action.value)

                case self._play_faction_selection:
                    self._process_faction_selection(action.index)

    def _process_main_selection(self, index: int):
        match index:
            case CapitalScene.MainChoice.SELECT_REGION.value:
                self._current_play = self._play_region_selection

            case CapitalScene.MainChoice.SELECT_FACTION.value:
                self._current_play = self._play_faction_selection

            case 3:
                self._raise_action(BeginSiegeAction(self))

            case _:
                self._current_play = None

    def _process_region_selection(self, index: int, region: str):
        if index == 0:
            self._current_play = self._play_main
        else:
            self._raise_action(MoveToRegionAction(self, region))

    def _process_faction_selection(self, index: int):
        if index == 0:
            self._current_play = self._play_main
        else:
            self._current_play = self._play_faction[index - 1]

    def _next(self) -> "Play":
        return self._current_play

    def _restart(self):
        super()._restart()
        self._current_play = self._play_main

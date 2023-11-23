from typing import TYPE_CHECKING

from Generation.faction import Faction

from Journey.Scenes.Scene import Scene
from Journey.Difficulty import Difficulty

from Journey.Plays.Play import Play
from Journey.Plays.Capital.MainPlay import MainPlay
from Journey.Plays.Capital.FactionSelectionPlay import FactionSelectionPlay
from Journey.Plays.Capital.RegionSelectionPlay import RegionSelectionPlay
from Journey.Plays.Capital.FactionPlay import FactionPlay

from Journey.Action import *

if TYPE_CHECKING:
    from Journey.Layout import Layout

class CapitalScene(Scene):
    _INDEX_MAIN = 0
    _INDEX_FACTION_SELECTION = 1
    _INDEX_REGION_SELECTION = 2
    _INDEX_START_FACTIONS = 3
    
    def __init__(self, parent: "Layout", factions: list[Faction], regions: list[str]):
        super().__init__(parent, None, Difficulty.Easy)
        self._plays.append(MainPlay(self))
        self._plays.append(FactionSelectionPlay(self, [faction.name for faction in factions]))
        self._plays.append(RegionSelectionPlay(self, regions))
        for faction in factions:
            self._plays.append(FactionPlay(self, parent.parent.character, parent.parent.scenario, faction))
        self._current_play = self._play_main

    @property
    def _play_main(self) -> MainPlay:
        return self._plays[CapitalScene._INDEX_MAIN]

    @property
    def _play_faction_selection(self) -> FactionSelectionPlay:
        return self._plays[CapitalScene._INDEX_FACTION_SELECTION]

    @property
    def _play_region_selection(self) -> RegionSelectionPlay:
        return self._plays[CapitalScene._INDEX_REGION_SELECTION]

    @property
    def _play_faction(self) -> list[FactionPlay]:
        return self._plays[CapitalScene._INDEX_START_FACTIONS:]

    def _process_RegionSelectionAction(self, action: RegionSelectionAction):
        self._current_play.stop()
        self._current_play = self._play_region_selection

    def _process_FactionSelectionAction(self, action: FactionSelectionAction):
        self._current_play.stop()
        self._current_play = self._play_faction_selection

    def _process_SelectedRegionAction(self, action: SelectedRegionAction):
        self._current_play.stop()
        self._raise_action(MoveToRegionAction(self, action.index - 1))

    def _process_SelectedFactionAction(self, action: SelectedFactionAction):
        self._current_play.stop()
        self._current_play = self._play_faction[action.index - 1]

    def _next(self) -> "Play":
        return self._current_play

    def _restart(self):
        super()._restart()
        self._current_play = self._play_main

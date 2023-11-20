from typing import TYPE_CHECKING

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
    
    # factions: not sure how to connect with the necassary npcs
    def __init__(self, parent: "Layout", factions: list[object], regions: list[str]):
        super().__init__(parent, None, Difficulty.Easy)
        self._plays.append(MainPlay(self))
        self._plays.append(FactionSelectionPlay(self, ["Faction A", "Faction B", "Faction C"]))
        self._plays.append(RegionSelectionPlay(self, regions))
        self._faction_plays = [FactionPlay(self, faction) for faction in factions]

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

    def _process_RegionSelectionAction(self, action: RegionSelectionAction):
        self._current_play = self._play_region_selection

    def _process_FactionSelectionAction(self, action: FactionSelectionAction):
        self._current_play = self._play_faction_selection

    def _process_SelectedFactionAction(self, action: SelectedFactionAction):
        pass

    def _next(self) -> "Play":
        return self._current_play

    def has_next(self) -> bool:
        return True

from typing import TYPE_CHECKING
import time

from Generation.scenario import Scenario, Kingdom, from_dict as scenario_from_dict
from Generation.faction import Faction, from_dict as faction_from_dict
from Generation.faction import create_factions


from Characters.character import Character
from Journey.Action import Action
from Journey.LoopManager import LoopManager

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import *
from Journey.Layout import Layout
from Journey.utility import to_dict, to_dict_index
from Journey.CapitalLayout import CapitalLayout

class Journey(BaseActionComponent, LoopManager):
    _NUMBER_OF_AREAS = 10

    def __init__(self, scenario: Scenario, factions: list[Faction], character: Character):
        BaseActionComponent.__init__(self, None, ActionConcern.Journey)
        LoopManager.__init__(self)

        self._scenario = scenario
        self._character = character
        self._factions = factions

        self._capital_layout = CapitalLayout(self)
        self._layouts = [Layout(self, region.name, region.description, Journey._NUMBER_OF_AREAS)
                         for region in self._scenario.kingdom.regions]
        self._nr_finished_layouts = 0

        self._current_layout = None

    def create_from_dict(state: dict) -> "Journey":
        journey = Journey.__new__(Journey)
        journey.__init_from_dict__(state)
        return journey

    def __init_from_dict__(self, state: dict):
        BaseActionComponent.__init__(self, None, ActionConcern.Journey)
        LoopManager.__init__(self)
        self._character = Character.create_from_dict(state["character"])
        self._scenario = scenario_from_dict(state["scenario"])
        self._factions = [faction_from_dict(faction) for faction in state["factions"]]
        self._nr_finished_layouts = state["number_of_finished_layouts"]
        self._capital_layout = CapitalLayout.create_from_dict(self, state["capital_layout"])
        self._layouts = [Layout.create_from_dict(self, layout_state) for layout_state in state["layouts"]]
        self._current_layout = None if state["current_layout"] is None \
                               else ([self._capital_layout] + self._layouts)[state["current_layout"]]


    def to_dict(self) -> dict:
        return {
            "character": to_dict(self._character),
            "scenario": to_dict(self._scenario),
            "factions": to_dict(self._factions),
            "number_of_finished_layouts": to_dict(self._nr_finished_layouts),
            "capital_layout": to_dict(self._capital_layout),
            "layouts": to_dict(self._layouts),
            "current_layout": to_dict_index(self._current_layout, [self._capital_layout] + self._layouts)
        }

    @property
    def factions(self) -> list[Faction]:
        return self._factions

    @property
    def current_layout(self):
        if self._nr_finished_layouts >= len(self._layouts): return self._layouts[-1]
        return self._layouts[self._nr_finished_layouts]

    @property
    def kingdom(self) -> "Kingdom":
        return self._scenario.kingdom

    @property
    def capital(self) -> str:
        return self._scenario.capital.name
    
    @property
    def character(self) -> Character:
        return self._character

    @property
    def scenario(self) -> Scenario:
        return self._scenario

    def _do_work(self):
        layout = self.next()
        layout.run()

    def next(self) -> Layout:
        if self._current_layout is None:
            self._current_layout = self._capital_layout
        return self._current_layout

    def _process_LayoutFinishedAction(self, action: LayoutFinishedAction):
        layout = action.layout
        if layout == self._current_layout:
            self._current_layout = self._capital_layout

    def _process_RefillHPAction(self, action: RefillHPAction):
        self._character.heal_percent(action.hp)

    def _process_ExpAction(self, action: ExpAction):
        self._character.gain_exp(action.exp)

    def _process_DamageAction(self, action: DamageAction):
        self._character.damage_percent(action.damage)
    
    def _process_LootAction(self, action: LootAction):
        pass # TODO: Add item to player

    def _process_MoveToRegionAction(self, action: MoveToRegionAction):
        self._current_layout.stop()
        self._current_layout = self._layouts[action.region]

    def _process_ReturnToCapitalAction(self, action: ReturnToCapitalAction):
        self._current_layout.stop()
        self._current_layout = self._capital_layout

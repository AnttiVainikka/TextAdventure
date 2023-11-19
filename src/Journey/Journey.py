from typing import TYPE_CHECKING

from Generation.scenario import Scenario, Kingdom, from_dict

from Characters.character import Character

from Journey.BaseActionComponent import BaseActionComponent
from Journey.Action import *
from Journey.Layout import Layout
from Journey.utility import to_dict

# TODO: Last layout could be the capital, where the end boss is the king
#
#       The base capital can also be a layout with a single scene, and different plays
#       (every play for a certain interaction)
#
#
class Journey(BaseActionComponent):
    _NUMBER_OF_AREAS = 10

    def __init__(self, scenario: Scenario, character: Character):
        super().__init__(None, ActionConcern.Journey)
        self._scenario = scenario
        self._character = character

        self._layouts = [Layout(self, region.name, region.description, Journey._NUMBER_OF_AREAS)
                         for region in self._scenario.kingdom.regions]
        self._nr_finished_layouts = 0

    def create_from_dict(state: dict) -> "Journey":
        journey = Journey.__new__(Journey)
        journey.__init_from_dict__(state)
        return journey

    def __init_from_dict__(self, state: dict):
        super().__init__(None, ActionConcern.Journey)
        self._character = Character.create_from_dict(state["character"])
        self._scenario = from_dict(state["scenario"])
        self._nr_finished_layouts = state["number_of_finished_layouts"]
        self._layouts = [Layout.create_from_dict(self, layout_state) for layout_state in state["layouts"]]

    def to_dict(self) -> dict:
        return {
            "character": to_dict(self._character),
            "scenario": to_dict(self._scenario),
            "number_of_finished_layouts": to_dict(self._nr_finished_layouts),
            "layouts": to_dict(self._layouts)
        }

    @property
    def is_finished(self) -> bool:
        return self._nr_finished_layouts == len(self._layouts)

    @property
    def current_layout(self) -> Layout:
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

    def has_next(self) -> bool:
        return self.current_layout != self._layouts[-1] or\
               not self.current_layout.is_finished

    def next(self) -> Layout:
        return self._layouts(self._nr_finished_layouts)

    def _process_LayoutFinishedAction(self, action: LayoutFinishedAction):
        layout = action.layout
        if self._nr_finished_layouts == len(self._layouts): return
        if layout == self.current_layout and layout.is_finished:
            self._nr_finished_layouts += 1

    def _process_RefillHPAction(self, action: RefillHPAction):
        self._character.heal_percent(action.hp)

    def _process_ExpAction(self, action: ExpAction):
        self._character.gain_exp(action.exp)

    def _process_DamageAction(self, action: DamageAction):
        self._character.damage_percent(action.damage)
    
    def _process_LootAction(self, action: LootAction):
        pass # TODO: Add item to player

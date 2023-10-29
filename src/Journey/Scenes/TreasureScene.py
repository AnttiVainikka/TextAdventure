from typing import TYPE_CHECKING
from random import randint

from Journey.Scenes.Scene import Scene
from Journey.Plays.TreasurePlay import *
from Journey.Difficulty import Difficulty
from Journey.Action import (
    OpenSacrificeChestAction,
    OpenFreeChestAction,
    OpenTrapChestAction,
    LeaveChestAction,
    SceneFinishedAction,
    DamageAction,
    LootAction
)

if TYPE_CHECKING:
    from Journey.Layout import Layout

class TreasureScene(Scene):
    _DIFFICULTY_TO_DAMAGE = {
        Difficulty.Easy: 1,
        Difficulty.Normal: 3,
        Difficulty.Hard: 5,
        Difficulty.Challenging: 10
    }

    def __init__(self, parent: "Layout", area: Area, difficulty: "Difficulty"):
        super().__init__(parent, area, difficulty)
        self._plays = []
        self._possible_loot = None

        match randint(0, 2):
            case 0:
                self._possible_loot = "Rusty Sword" # TODO: generate a loot using region based loot generation -> needs character class
                self._plays.append(FreeTreasurePlay(self, parent.name, parent.description, area, str(self._possible_loot)))
            case 1:
                self._plays.append(TrapTreasurePlay(self, parent.name, parent.description, area))
            case 2:
                self._possible_loot = "Rusty Sword" # TODO: generate a loot using region based loot generation -> needs character class
                self._plays.append(SacrificeTreasurePlay(self, parent.name, parent.description, area, str(self._possible_loot)))

    def __init_from_dict__(self, parent: "Layout", state: dict):
        super().__init_from_dict__(parent, state)
        self._possible_loot = state["possible_loot"] # TODO: Adjust loot

    def to_dict(self) -> dict:
        state = super().to_dict()
        state["possible_loot"] = to_dict(self._possible_loot)
        return state

    def _next(self) -> "TreasurePlay":
        return self._plays[0]

    def has_next(self) -> bool:
        return self._current_play != self._plays[0]

    def _process_OpenSacrificeChestAction(self, action: OpenSacrificeChestAction):
        self._raise_action(DamageAction(self, TreasureScene._DIFFICULTY_TO_DAMAGE[self._difficulty]))
        self._raise_action(LootAction(self, self._possible_loot))
        self._is_finished = True
        self._raise_action(SceneFinishedAction(self))

    def _process_OpenFreeChestAction(self, action: OpenFreeChestAction):
        self._raise_action(LootAction(self, self._possible_loot))
        self._is_finished = True
        self._raise_action(SceneFinishedAction(self))

    def _process_OpenTrapChestAction(self, action: OpenTrapChestAction):
        self._raise_action(DamageAction(self, TreasureScene._DIFFICULTY_TO_DAMAGE[self._difficulty]))
        self._is_finished = True
        self._raise_action(SceneFinishedAction(self))

    def _process_LeaveChestAction(self, action: LeaveChestAction):
        self._is_finished = True
        self._raise_action(SceneFinishedAction(self))

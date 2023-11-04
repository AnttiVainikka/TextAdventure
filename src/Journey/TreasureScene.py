from Journey.Scene import Scene
from Journey.TreasurePlay import TreasurePlay, LootedTreasurePlay
from Journey.Circumstance import Circumstances

class TreasureScene(Scene):
    _DEFAULT_PLAY = 0
    _LOOTED_PLAY = 1

    def __init__(self, parent, difficulty, circumstances: Circumstances):
        super().__init__(parent, difficulty, circumstances)
        self._possible_loot = "Rusty Sword" # TODO: generate a loot (probably based on scene difficulty)
        self._is_looted = False
        self._plays = [TreasurePlay(self), LootedTreasurePlay(self)]

    @property
    def possible_loot(self):
        return self._possible_loot

    @property
    def is_looted(self) -> bool:
        return self._is_looted

    @property
    def play(self) -> TreasurePlay:
        return self._plays[TreasureScene._LOOTED_PLAY if self._is_looted else TreasureScene._DEFAULT_PLAY]            

    @property
    def is_finished(self) -> bool:
        return True
    
    # Can also be used to create looted scenes by default
    def loot(self):
        self._is_looted = True

from typing import TYPE_CHECKING
from Journey.Plays.Play import Play

# Need import these so the runtime can recognize the types
from Journey.Plays.IntroPlay import IntroPlay
from Journey.Plays.RiddlePlay import RiddlePlay
from Journey.Plays.TreasurePlay import *
from Journey.Plays.RestPlay import RestPlay
from Journey.Plays.BattlePlay import BattlePlay
from Journey.Plays.FinalBattlePlay import FinalBattlePlay
from Journey.Plays.OutroPlay import OutroPlay
from Journey.Plays.Capital.FactionPlay import FactionPlay
from Journey.Plays.Capital.MainPlay import MainPlay
from Journey.Plays.Capital.RegionSelectionPlay import RegionSelectionPlay
from Journey.Plays.Capital.FactionSelectionPlay import FactionSelectionPlay


if TYPE_CHECKING:
    from Journey.Scenes.Scene import Scene

def create_from_dict(parent: "Scene", state: dict) -> "Play":
    if state == None: return None
    play_cls = globals()[state["type"]]
    if play_cls is not None:
        play = play_cls.__new__(play_cls)
        play.__init_from_dict__(parent, state)
        return play
    return None

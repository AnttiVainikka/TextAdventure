from typing import TYPE_CHECKING
from Journey.Scenes.Scene import Scene
from Journey.Scenes.IntroScene import IntroScene
from Journey.Scenes.RiddleScene import RiddleScene
from Journey.Scenes.TreasureScene import TreasureScene
from Journey.Scenes.RestScene import RestScene
from Journey.Scenes.BattleScene import BattleScene
from Journey.Scenes.FinalBattleScene import FinalBattleScene
from Journey.Scenes.OutroScene import OutroScene

if TYPE_CHECKING:
    from Journey.Layout import Layout

def create_from_dict(parent: "Layout", state: dict) -> Scene:
    if state == None: return None
    scene_cls = globals()[state["type"]]
    if scene_cls is not None:
        scene = scene_cls.__new__(scene_cls)
        scene.__init_from_dict__(parent, state)
        return scene
    return None

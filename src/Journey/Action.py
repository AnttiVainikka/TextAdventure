from typing import TYPE_CHECKING
from enum import Flag, auto, Enum

if TYPE_CHECKING:
    from Journey.Plays.Play import Play
    from Journey.Scenes.Scene import Scene
    from Journey.Interaction import Interaction
    from Journey.Layout import Layout

class ActionConcern(Flag):
    Interaction = auto()
    Play = auto()
    Scene = auto()
    Layout = auto()
    Journey = auto()

class Action:
    def __init__(self, concern: ActionConcern):
        self.concern: ActionConcern = concern

class Actions(list):
    def __init__(self, iterable):
        super().__init__(self._validate(val) for val in iterable)

    def __setitem__(self, index, item):
        super().__setitem__(index, self._validate(item))

    def insert(self, index, item):
        super().insert(index, self._validate(item))

    def append(self, item):
        super().append(self._validate(item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(self._validate(item) for item in other)

    def is_concern(self, flag: ActionConcern) -> bool:
        return len(self.specific(flag)) != 0

    def specific(self, flag: ActionConcern) -> "Actions":
        return Actions([action for action in self if flag in action.concern])

    def _validate(self, val):
        if isinstance(val, Action):
            return val
        raise TypeError(f"Expected type Action. Received {type(val)}")

##################
##### LAYOUT #####
class LayoutAction(Action):
    def __init__(self, layout: "Layout", action_concern: ActionConcern = ActionConcern.Journey):
        super().__init__(action_concern)
        self.layout = layout

class LayoutFinishedAction(LayoutAction):
    pass

#################
##### SCENE #####
class SceneAction(Action):
    def __init__(self, scene: "Scene", action_concern: ActionConcern = ActionConcern.Layout):
        super().__init__(action_concern)
        self.scene = scene

class SceneFinishedAction(SceneAction):
    pass

class EnterRegionAction(SceneAction):
    pass

class ReturnToCapitalAction(SceneAction):
    def __init__(self, scene: "Scene"):
        super().__init__(scene, ActionConcern.Journey)

class ExpAction(SceneAction):
    def __init__(self, scene: "Scene", exp: int):
        super().__init__(scene, ActionConcern.Journey)
        self.exp = exp

class DamageAction(SceneAction):
    def __init__(self, scene: "Scene",damage: float):
        super().__init__(scene, ActionConcern.Journey)
        self.damage = damage

class LootAction(SceneAction):
    def __init__(self, scene: "Scene",item: object):
        super().__init__(scene, ActionConcern.Journey)
        self.item = item

class RefillHPAction(SceneAction):
    def __init__(self, scene: "Scene", hp: float):
        super().__init__(scene, ActionConcern.Journey)
        self.hp = hp

class MoveToRegionAction(SceneAction):
    def __init__(self, scene: "Scene", region: str):
        super().__init__(scene, ActionConcern.Journey)
        self.region = region

################
##### PLAY #####
class PlayAction(Action):
    def __init__(self, play: "Play", action_concern: ActionConcern = ActionConcern.Scene):
        super().__init__(action_concern)
        self.play = play

class PlayFinishedAction(PlayAction):
    pass        

class StartBattleAction(PlayAction):
    pass

class IntroLeaveAction(PlayAction):
    pass

class IntroEnterAction(PlayAction):
    pass

class RiddleGoodAnswerAction(PlayAction):
    pass

class RiddleWrongAnswerAction(PlayAction):
    pass

class OpenTrapChestAction(PlayAction):
    pass

class OpenFreeChestAction(PlayAction):
    pass

class OpenSacrificeChestAction(PlayAction):
    pass

class LeaveChestAction(PlayAction):
    pass
        
class RestAction(PlayAction):
    pass

class SkipAction(PlayAction):
    pass

class SelectionAction(PlayAction):
    def __init__(self, play: "Play", index: int, value: str):
        super().__init__(play)
        self.index = index
        self.value = value

#######################
##### INTERACTION #####
class InteractionAction(Action):
    def __init__(self, interaction: "Interaction", action_concern: ActionConcern = ActionConcern.Play):
        super().__init__(action_concern)
        self.interaction = interaction

class InteractionAnsweredAction(InteractionAction):
    pass

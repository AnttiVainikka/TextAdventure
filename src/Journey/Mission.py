from abc import ABC

from Generation.mission import generate

from Journey.utility import to_dict

class Mission(ABC):
    def __init__(self, description: str, quest_description: str, objective: str):
        self.description = description
        self.quest_description = quest_description
        self.objective = objective

    def __init_from_dict__(self, state: dict):
        self.description = state["description"]
        self.quest_description = state["quest_description"]
        self.objective = state["objective"]

    def create_from_dict(state: dict) -> "Mission":
        mission_cls = globals()[state["type"]]
        if mission_cls is not None:
            mission = mission_cls.__new__(mission_cls)
            mission.__init_from_dict__(state)
            return mission
        return None

    def to_dict(self) -> dict:
        return {
            "type": to_dict(type(self).__name__),
            "description": to_dict(self.description),
            "quest_description": to_dict(self.quest_description),
            "objective": to_dict(self.objective)
        }

class ArtifactMission(Mission):
    TYPE = "Artifact"
    GOAL = "Collect a certain artifact"

    def __init__(self, description: str, quest_description: str, objective: str):
        super().__init__(description, quest_description, objective)

    def generate(kingdom_name: str, kingdom_description: str, region_name: str) -> "ArtifactMission":
        return ArtifactMission(*(generate(kingdom_name, kingdom_description, region_name, ArtifactMission.TYPE, ArtifactMission.GOAL)))

class TargetMission(Mission):
    TYPE = "Target"
    GOAL = "Kill a certain foe"

    def __init__(self, description: str, quest_description: str, objective: str):
        super().__init__(description, quest_description, objective)

    def generate(kingdom_name: str, kingdom_description: str, region_name: str) -> "TargetMission":
        return TargetMission(*(generate(kingdom_name, kingdom_description, region_name, TargetMission.TYPE, TargetMission.GOAL)))

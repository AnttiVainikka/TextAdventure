from Generation.generator import llm_create
from Generation.scenario import Region
from dataclasses import dataclass
from Journey.Mission import Mission

@dataclass
class Area:
    name: str
    description: str

def generate(kingdom_name: str, region_name: str, region_description: str, mission_description: str, number_of_areas: int = 10) -> list[Area]:
    area_strings = llm_create('area/init', 1, kingdom_name=kingdom_name,
                                              region_name=region_name,
                                              region_description=region_description,
                                              region_mission=mission_description,
                                              number_of_areas=number_of_areas)[0].areas
    areas = []
    for area_string in area_strings:
        splits = area_string.split(":", 1)
        if len(splits) == 2:
            name:str = splits[0]
            description = splits[1]
            name.lstrip()
            description.lstrip()
            while name[0].isdigit():
                name = name[1:]

            if name[0] == ".":
                name = name[1:]

            areas.append(Area(name, description))
    return areas

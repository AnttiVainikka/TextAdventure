from Generation.generator import llm_create

def generate(kingdom_name: str, kingdom_description: str, region_name: str, mission_type: str, mission_goal: str) -> (str, str, str):
    mission = llm_create('mission/init', kingdom_name=kingdom_name, 
                                         kingdom_description=kingdom_description,
                                         region_name=region_name,
                                         mission_type=mission_type,
                                         mission_goal=mission_goal)[0].mission
    quest = llm_create('mission/quest', kingdom_name=kingdom_name,
                                        region_name=region_name,
                                        mission=mission,
                                        mission_type=mission_type)[0].quest
    
    objective = llm_create('mission/objective', mission_type=mission_type,
                                                mission_goal=mission_goal,
                                                quest_description=quest)[0].objective_entity
    
    return (mission, quest, objective)

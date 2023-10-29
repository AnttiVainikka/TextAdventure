from Generation.generator import llm_create

def generate(region_name: str, mission_description: str, capital_name: str) -> str:
    return llm_create("outro_scene", region_name=region_name,
                                     mission_description=mission_description,
                                     capital_name=capital_name)[0].context

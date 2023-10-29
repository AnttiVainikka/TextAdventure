from Generation.generator import llm_create

def generate(region: str, region_description: str, mission: str) -> str:
    return llm_create("intro_scene", region=region, region_description=region_description, mission=mission)[0].context

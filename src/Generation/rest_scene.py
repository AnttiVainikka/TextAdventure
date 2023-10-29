from Generation.generator import llm_create


def generate_intro_context(region_name: str, region_description: str, area_name: str, area_description: str) -> str:
    return llm_create('rest_scene/intro', region_name=region_name,
                                          region_description=region_description,
                                          area_name=area_name,
                                          area_description=area_description)[0].context

def generate_outro_leave_context(area_name: str, area_context: str) -> str:
    return llm_create('rest_scene/outro/leave', area_name=area_name,
                                                area_context=area_context)[0].context

def generate_outro_rest_context(area_name: str, area_context: str) -> str:
    return llm_create('rest_scene/outro/rest', area_name=area_name,
                                               area_context=area_context)[0].context
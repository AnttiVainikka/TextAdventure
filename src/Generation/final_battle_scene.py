from Generation.generator import llm_create
from Generation.summarize_context import summarize_context

def generate_intro(region_name: str, area_name: str, area_description: str, mission_quest: str, boss_name: str) -> str:
    return llm_create('final_battle_scene/intro', region_name=region_name,
                                                  area_name=area_name,
                                                  area_description=area_description,
                                                  mission_quest=mission_quest,
                                                  boss_name=boss_name)[0].context

def generate_intro_p2(region_name: str, area_name: str, area_context: str, mission_quest: str, boss_name: str) -> str:
    _area_context = summarize_context(area_context)
    return llm_create('final_battle_scene/intro_p2', region_name=region_name,
                                                     area_name=area_name,
                                                     area_context=_area_context,
                                                     mission_quest=mission_quest,
                                                     boss_name=boss_name)[0].context

def generate_outro(region_name: str, area_name: str, area_context: str, mission_quest: str, boss_name: str):
    _area_context = summarize_context(area_context)
    return llm_create('final_battle_scene/outro', region_name=region_name,
                                                  area_name=area_name,
                                                  area_context=_area_context,
                                                  mission_quest=mission_quest,
                                                  boss_name=boss_name)[0].context

def generate_outro_p2(region_name: str, area_name: str, area_context: str, mission_quest: str, boss_name: str):
    _area_context = summarize_context(area_context)
    return llm_create('final_battle_scene/outro_p2', region_name=region_name,
                                                     area_name=area_name,
                                                     area_context=_area_context,
                                                     mission_quest=mission_quest,
                                                     boss_name=boss_name)[0].context

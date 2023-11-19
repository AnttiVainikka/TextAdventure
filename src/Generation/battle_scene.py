from Generation.generator import llm_create
from Generation.enemy_type import EnemyType

def generate_intro_context(region_name: str,
                           region_description: str,
                           area_name: str,
                           area_description: str,
                           enemy_types: list[EnemyType],
                           leader_type: EnemyType = None) -> str:
    return llm_create('battle_scene/intro', region_name=region_name,
                                            region_description=region_description,
                                            area_name=area_name,
                                            area_description=area_description,
                                            enemy_types=_enemy_text(enemy_types, leader_type))[0].context

def generate_outro_context(region_name: str,
                           region_description: str,
                           area_name: str,
                           area_description: str,
                           enemy_types: list[EnemyType],
                           leader_type: EnemyType = None) -> str:
    return llm_create('battle_scene/outro', region_name=region_name,
                                            region_description=region_description,
                                            area_name=area_name,
                                            area_description=area_description,
                                            enemy_types=_enemy_text(enemy_types, leader_type))[0].context

def _enemy_text(enemy_types: list[EnemyType], leader_type: EnemyType) -> str:
    if len(enemy_types) == 1: return enemy_types[0]
    s = enemy_types[0].name
    for enemy_type in enemy_types[1:-1]:
        s += ", " + enemy_type.name
    
    if leader_type is None:
        s += " and " + enemy_types[-1].name
    else:
        s += ", " + enemy_types[-1].name
        s += " and their leader " + leader_type.name
    return s

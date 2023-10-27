import Characters.skill as skill
from Generation.generator import llm_create

def generate(user_class: str, skill_type: str, skill_nature: str, skill_rarity: str, skill_target: str):
    data = llm_create('skill', count=1, classtype=user_class,
                                        type=skill_type,
                                        nature=skill_nature,
                                        rarity=skill_rarity,
                                        target=skill_target)[0]
    return (data.name, data.description)

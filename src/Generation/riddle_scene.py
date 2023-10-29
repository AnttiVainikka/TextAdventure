from Generation.generator import llm_create

def generate_intro_context(region_name: str, region_description: str, area_name: str, area_description: str) -> str:
    return llm_create("riddle_scene/intro", region_name=region_name,
                                            region_description=region_description,
                                            area_name=area_name,
                                            area_description=area_description)[0].context

def generate_riddle(area_name: str, intro_context: str, riddle_difficulty: str) -> (str, str):
    data = llm_create("riddle_scene/riddle", area_name=area_name,
                                             intro_context=intro_context,
                                             riddle_difficulty=riddle_difficulty)[0]
    return (data.riddle, data.answer)

def check_answer(riddle: str, riddle_answer: str, player_answer: str) -> bool:
    return llm_create("riddle_scene/check", riddle=riddle,
                                            riddle_answer=riddle_answer,
                                            player_answer=player_answer)[0].is_it_correct

def generate_wrong_answer_context(area_name: str, intro_context: str, riddle: str, riddle_answer: str) -> str:
    return llm_create("riddle_scene/wrong_answer", area_name=area_name,
                                                   intro_context=intro_context,
                                                   riddle=riddle,
                                                   riddle_answer=riddle_answer)[0].context

def generate_good_answer_context(area_name: str, intro_context: str, riddle: str, riddle_answer: str) -> str:
    return llm_create("riddle_scene/good_answer", area_name=area_name,
                                                  intro_context=intro_context,
                                                  riddle=riddle,
                                                  riddle_answer=riddle_answer)[0].context

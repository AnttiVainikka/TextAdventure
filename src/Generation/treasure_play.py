from Generation.generator import llm_create

def generate_context(intuitions: str) -> (str, str, str):
    data = llm_create('treasure_play/context', 1, intuition=intuitions)[0].model_dump()
    return (data['context'], data['look_around_choice'], data['do_nothing_choice'])

def generate_closure(context: str, choice: str, loot: str) -> str:
    data = llm_create('treasure_play/closure', 1, context=context, choice=choice, loot=loot)[0].model_dump()
    return data['closure']

def generate_looted_context(context: str) -> (str, str, str):
    data = llm_create('treasure_play/looted_context', 1, context=context)[0].model_dump()
    return (data['looted_context'], data['look_around_choice'], data['do_nothing_choice'])

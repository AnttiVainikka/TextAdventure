from Generation.generator import llm_create

def generate_free_intro_context(region_name: str, region_description: str, area_name: str, area_description: str) -> str:
    return llm_create("treasure_scene/intro/free", region_name=region_name,
                                                   region_description=region_description,
                                                   area_name=area_name,
                                                   area_description=area_description)[0].context

def generate_free_outro_open_context(area_name: str, area_context: str, item: str) -> str:
    return llm_create("treasure_scene/outro/open/free", area_name=area_name,
                                                        area_context=area_context,
                                                        item=item)[0].context

def generate_free_outro_leave_context(area_name: str, area_context: str) -> str:
    return llm_create("treasure_scene/outro/leave/free", area_name=area_name,
                                                         area_context=area_context)[0].context

def generate_sacrifice_intro_context(region_name: str, region_description: str, area_name: str, area_description: str) -> str:
    return llm_create("treasure_scene/intro/sacrifice", region_name=region_name,
                                                   region_description=region_description,
                                                   area_name=area_name,
                                                   area_description=area_description)[0].context

def generate_sacrifice_outro_open_context(area_name: str, area_context: str, item: str) -> str:
    return llm_create("treasure_scene/outro/open/sacrifice", area_name=area_name,
                                                        area_context=area_context,
                                                        item=item)[0].context

def generate_sacrifice_outro_leave_context(area_name: str, area_context: str) -> str:
    return llm_create("treasure_scene/outro/leave/sacrifice", area_name=area_name,
                                                         area_context=area_context)[0].context

def generate_trap_intro_context(region_name: str, region_description: str, area_name: str, area_description: str) -> str:
    return llm_create("treasure_scene/intro/trap", region_name=region_name,
                                                   region_description=region_description,
                                                   area_name=area_name,
                                                   area_description=area_description)[0].context

def generate_trap_outro_open_context(area_name: str, area_context: str) -> str:
    return llm_create("treasure_scene/outro/open/trap", area_name=area_name,
                                                        area_context=area_context)[0].context

def generate_trap_outro_leave_context(area_name: str, area_context: str) -> str:
    return llm_create("treasure_scene/outro/leave/trap", area_name=area_name,
                                                         area_context=area_context)[0].context


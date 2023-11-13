from concurrent import futures
from dataclasses import dataclass
import json
from multiprocessing.pool import ThreadPool
import random

from Generation.generator import llm_create

@dataclass
class Kingdom:
    name: str
    geography: str
    economy: str
    description: str

@dataclass
class Ruler:
    title: str
    name: str
    backstory: str
    deeds: str
    personality: str
    evil_deeds: str
    governance_style: str

@dataclass
class CapitalCity:
    name: str
    population: str
    architecture: str
    history: str

@dataclass
class Scenario:
    kingdom: Kingdom
    ruler: Ruler
    capital: CapitalCity

ruler_backgrounds = [
    'no-one special',
    'a heir to a minor noble family',
    'a wealthy merchant with no political aspirations',
    'the youngest child in the royal family',
    'a street urchin with a brilliant mind',
    'a shopkeeper'
]

ruler_personalities = [
    'They used to be a genuinely good person - this it what makes it so tragic.',
    'They were quite happy minding their own business, not caring what others thought.',
    'They were not exactly a good person, but would have balked at the things they did themself later.',
    'They were selfish, even back then, though not nearly as much as nowadays.',
    'They were, frankly, a terrible person. But back them, they could only do so much harm.'
]

ruler_crises = [
    'the kingdom was truck by a terrible natural disaster. Someone just had to step up, and do what was necessary.',
    'a neighbouring kingdom attacked. Neither the army or the King leading it were competent, so someone else had to step up.'
    'the King died in accident without leaving a heir. The noble families decided to vote on the issue.',
    'the King was assassinated. Naturally, all of the noble families blamed each other.',
]

ruler_gender = ['male', 'female', 'other']

def _pick_random(items: list):
    idx = random.randint(0, len(items) - 1)
    return items[idx]

def _new_ruler(kingdom_name: str, kingdom_desc: str) -> Ruler:
    # Pick background, original personality and the crisis from human-written random options
    background_choice = _pick_random(ruler_backgrounds)
    personality = _pick_random(ruler_personalities)
    crisis = _pick_random(ruler_crises)

    # Randomly pick a gender and title based on it
    gender = _pick_random(ruler_gender)
    title = 'King' if gender != 'female' else 'Queen' # TODO multiple title options

    # Generate a set of names and pick one of them
    names = llm_create('ruler_names', background=background_choice, gender=gender)[0]
    name = _pick_random(names.names)

    # Generate backstory for the ruler
    background = llm_create('ruler_background', kingdom=kingdom_name, details=kingdom_desc, title=title, name=name,
                            background=background_choice, personality=personality, crisis=crisis)[0]
    backstory=f'{background.origin} {background.crisis} {background.rise_to_power}\n\n{background.motivation}'

    # And finally, the up-to-date details of them
    tyrant = llm_create('tyrant', kingdom=kingdom_name, details=kingdom_desc, title=title, name=name, backstory=backstory)[0]
    return Ruler(title, name, backstory, tyrant.deeds, tyrant.personality, tyrant.evil_deeds, tyrant.governance_style)

def _new_scenario(kingdom) -> Scenario:
    # Create ruler and capital based on kingdom blurb (mostly to introduce more randomness to LLMs)
    with futures.ThreadPoolExecutor() as executor:
        ruler = _new_ruler(kingdom.name, f'{kingdom.geography} {kingdom.economy}')
        capital_future = executor.submit(llm_create, 'capital_city',
                                         kingdom=kingdom.name,
                                         kingdom_details=f'{kingdom.geography} {kingdom.economy}',
                                         ruler_personality=ruler.personality,
                                         ruler_evil=ruler.evil_deeds,
                                         governance_style=ruler.governance_style
                                         )
        
        # Rewrite kingdom details to account for the new ruler's deeds
        rewrite = llm_create('kingdom_rewrite',
                                        kingdom=json.dumps(kingdom.dict(), indent=2),
                                        ruler_title=ruler.title,
                                        ruler_name=ruler.name,
                                        ruler_desc=f'{ruler.deeds} {ruler.governance_style}'
                                        )[0]
        capital = capital_future.result()[0]
    return Scenario(
        Kingdom(rewrite.name, rewrite.geography, rewrite.economy, f'{rewrite.geography} {rewrite.economy}'),
        ruler,
        CapitalCity(capital.name, capital.population, capital.architecture, capital.history))


def new_scenarios(count: int) -> list[Scenario]:
    scenarios = []
    kingdoms = llm_create('kingdom', count)

    # Note: can't parallelize this, OpenAI client seems to dislike multithreading
    with ThreadPool() as pool:
        for scenario in pool.map(_new_scenario, kingdoms):
            scenarios.append(scenario)

    return scenarios
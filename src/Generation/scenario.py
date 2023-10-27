from dataclasses import dataclass

from Generation.generator import llm_create

@dataclass
class Kingdom:
    name: str
    geography: str
    economy: str
    description: str

@dataclass
class Ruler:
    name: str
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

def new_scenarios(count: int) -> list[Scenario]:
    scenarios = []
    # TODO parallelize this to improve generation speed
    kingdoms = llm_create('kingdom', count)
    for kingdom in kingdoms:
        tyrant = llm_create('tyrant', kingdom=kingdom.name, details=f'{kingdom.geography} {kingdom.economy}', ruler=kingdom.ruler_name)[0]
        capital = llm_create('capital_city',
                            kingdom=kingdom.name,
                            kingdom_details=f'{kingdom.geography} {kingdom.economy}',
                            ruler_personality=tyrant.personality,
                            ruler_evil=tyrant.evil_deeds,
                            governance_style=tyrant.governance_style)[0]
        scenarios.append(Scenario(
            Kingdom(kingdom.name, kingdom.geography, kingdom.economy, f'{kingdom.geography} {kingdom.economy}'),
            Ruler(kingdom.ruler_name, tyrant.personality, tyrant.evil_deeds, tyrant.governance_style),
            CapitalCity(capital.name, capital.population, capital.architecture, capital.history)))
    return scenarios
        


import json
import os

from Journey.Journey import Journey
from Journey.utility import to_dict
from Characters.character import Character
from Characters.create import create_main_character
from Generation.scenario import Scenario, new_scenarios, from_dict as scenario_from_dict

from Generation.faction import Faction, create_factions, from_dict as faction_from_dict

import log

_logger = log.getLogger(__name__)

def dump_scenario(idx:int, scenario: Scenario):
    print(f'{idx}. {scenario.capital.name}, Kingdom of {scenario.kingdom.name}')
    print(f'Ruled by: {scenario.ruler.title} {scenario.ruler.name}')
    print(scenario.kingdom.description, '\n')
    print(scenario.ruler.governance_style, scenario.ruler.evil_deeds)
    for region in scenario.kingdom.regions:
        print(f'Region {region.name}')
        print(region.description)

class Game:
    _SAVES_DIR = "saves/"
    _SAVES_SCENARIOS_DIR = _SAVES_DIR + "scenarios/"
    _SAVES_FACTIONS_DIR = _SAVES_DIR + "factions/"

    def __init__(self, save_file: str = None):
        self.journey: Journey = None
        if save_file is not None:
            self.journey = Journey.create_from_dict(json.load(open(save_file, "r")))

    def create_character(self) -> Character:
        return create_main_character() # TODO: Create this properly so the player can actaully create/select a character

    def create_scenarios():
        scenarios = new_scenarios(3)
        for scenario in scenarios:
            _logger.info("Generating scenario...")
            open(f"{Game._SAVES_SCENARIOS_DIR}{scenario.kingdom.name}.json", "w").write(json.dumps(to_dict(scenario), indent=4))
            _logger.info(f"Generation of scenario {scenario.kingdom.name} has finished")

    def create_faction(scenario: Scenario):
        _logger.info("Generating factions...")
        factions = create_factions(scenario)
        open(f"{Game._SAVES_FACTIONS_DIR}{scenario.kingdom.name}.json", "w").write(json.dumps(to_dict(factions), indent=4))
        _logger.info(f"Generation of factions has finished")

    def select_scenario() -> (Scenario, list[Faction]):
        scenarios = os.listdir(Game._SAVES_SCENARIOS_DIR)
        if scenarios == []:
            Game.create_scenarios()
        scenarios = os.listdir(Game._SAVES_SCENARIOS_DIR)
        scenarios = [scenario_from_dict(json.load(open(f"{Game._SAVES_SCENARIOS_DIR}{scenario}", "r"))) \
                     for scenario in scenarios]

        for idx, scenario in enumerate(scenarios):
            dump_scenario(idx, scenario)
            print("-"*80)

        selected = int(input('Choose the scenario: '))
        scenario = scenarios[selected]

        factions = os.listdir(Game._SAVES_FACTIONS_DIR)
        faction_file_name = scenario.kingdom.name + ".json"
        if faction_file_name not in factions:
            Game.create_faction(scenario)
        faction_file = os.listdir(Game._SAVES_FACTIONS_DIR)[0]
        factions = json.load(open(f"{Game._SAVES_FACTIONS_DIR}{faction_file}", "r"))
        factions = [faction_from_dict(faction) for faction in factions]
        return (scenario, factions)

    def start(self):
        if self.journey is None:
            scenario, factions = Game.select_scenario()
            character = self.create_character()
            self.journey = Journey(scenario, factions, character)

        # TODO: Some welcome message?

        self.journey.run()

game = Game("saves/test_journey.json")
game.start()

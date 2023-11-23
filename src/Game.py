import json
import time

from Journey.Journey import Journey
from Characters.character import Character
from Characters.create import create_main_character
from Generation.scenario import Scenario, new_scenarios

class Game:
    def __init__(self, save_file: str = None):
        self.journey: Journey = None
        if save_file is not None:
            self.journey = Journey.create_from_dict(json.load(open(save_file, "r")))

    def create_character(self) -> Character:
        return create_main_character() # TODO: Create this properly so the player can actaully create/select a character

    def create_scenario(self) -> Scenario:
        return new_scenarios(1)

    def start(self):
        if self.journey is None:
            scenario = self.create_scenario()
            character = self.create_character()
            self.journey = Journey(scenario, character)

        # TODO: Some welcome message?

        self.journey.run()

game = Game("test_journey.json")
game.start()

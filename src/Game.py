import json
import os

from Journey.Journey import Journey
from Journey.utility import to_dict
from Characters.character import Character
from Characters.create import create_character as create_player_character
from Generation.scenario import Scenario, new_scenarios, from_dict as scenario_from_dict
from Generation.faction import Faction, create_factions, from_dict as faction_from_dict

import UI
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
    _SAVES_JOURNEY_DIR = _SAVES_DIR + "journey/"
    _SAVES_SCENARIOS_DIR = _SAVES_DIR + "scenarios/"
    _SAVES_FACTIONS_DIR = _SAVES_DIR + "factions/"
    _SAVES_CHARACTERS_DIR = _SAVES_DIR + "characters/"

    def __init__(self):
        self._journey: Journey = None
        self._scenario: Scenario = None
        self._factions: list[Faction] = None
        self._character: Character = None

        self._main_menu = UI.Menu("Select option:", [
            UI.MenuOption("New Game", self._new_game),
            UI.MenuOption("Load Game", self._load_game),
            UI.MenuOption("Quit Game", self._quit_game)
        ])

    def main_menu(self):
        return self._main_menu

    def _quit_game(self):
        UI.clear()
        exit(0)

    def _create_character(self):
        UI.clear()
        UI.print_title()
        UI.print("[blue]Character creation")
        UI.print()
        UI.print("[green]Name: [white]", end="")
        name = UI.input()
        UI.print()
        UI.print("[green]Description: [white]", end="")
        description = UI.input()
        UI.print()
        cls = UI.Menu("Select class", [
            UI.MenuOption("Warrior", "warrior"),
            UI.MenuOption("Mage", "mage"),
            UI.MenuOption("Rogue", "rogue")],
            integrated=True
            ).select()
        
        UI.clear()
        UI.print_title()
        self._character = UI.work_with_spinner("Creating character", create_player_character, name, description, cls, 5, 4)
    
    def _create_factions(self):
        if self._scenario is not None:
            UI.clear()
            UI.print_title()
            self._factions = UI.work_with_spinner("Generating factions", create_factions, self._scenario)

    def _create_journey(self):
        if self._scenario is not None and \
           self._factions is not None and \
           self._character is not None:
            UI.clear()
            UI.print_title()
            self._journey = UI.work_with_spinner("Creating map", Journey, self._scenario, self._factions, self._character)

    def _save_journey(self):
        if self._journey is not None:
            name = self._journey.kingdom.name
            open(f"{Game._SAVES_JOURNEY_DIR}{name}.json", "w").write(json.dumps(self._journey.to_dict(), indent=4))

    def _new_game(self):
        is_selected = False
        while not is_selected:
            UI.clear()
            UI.print_title()
            scenarios = UI.work_with_spinner("Generating scenario", new_scenarios, 1)
            menu = UI.Menu("Do you want to play this scenario?", [
                UI.MenuOption("Accept scenario", 1),
                UI.MenuOption("Create new scenario", 2)
            ],  UI.MenuOption("Back", self.main_menu), additional=UI.scenario_to_string(scenarios[0]))
            selected = menu.select()
            if selected == 1:
                self._scenario = scenarios[0]
                self._create_factions()
                self._create_character()
                self._create_journey()
                self._save_journey()
                is_selected = True
            elif selected == 2:
                pass
            else:
                return selected
        return self.main_menu()
        
    def _load_game(self):
        saves = os.listdir(Game._SAVES_JOURNEY_DIR)
        saves = [save for save in saves if save.endswith('.json')]
        save_names = [os.path.splitext(save)[0] for save in saves]

        return UI.Menu("Select game: ", [
            UI.MenuOption(save, self._load, save=save) for save in save_names],
            UI.MenuOption("Back", self.main_menu)
        )

    def _load(self, save: str):
        self._journey = Journey.create_from_dict(json.load(open(f"{Game._SAVES_JOURNEY_DIR}{save}.json", "r")))

    def start(self):
        while True:
            self._journey = None
            UI.rollback_manager.set_level(0)
            UI.rollback()        
            callback = self._main_menu.select()

            while self._journey is None:
                if isinstance(callback, UI.Menu):
                    callback = callback.select()

            # RUN GAME
            UI.clear()
            self._journey.run()


game = Game()
game.start()

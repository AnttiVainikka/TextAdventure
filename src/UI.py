from rich.console import Console
from rich.style import Style
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from pynput import keyboard
from typing import Any, Callable
from Generation.scenario import Scenario
import time
import pyfiglet

console = Console()

_TITLE = r"""
 [red]______       _  [green] _______        _   [blue]            _                 _                  
[red]|  ____|     (_) [green]|__   __|      | |  [blue]   /\      | |               | |                 
[red]| |__   _ __  _  ___[green]| | _____  _| |_ [blue]  /  \   __| |_   _____ _ __ | |_ _   _ _ __ ___ 
[red]|  __| | '_ \| |/ __[green]| |/ _ \ \/ / __|[blue] / /\ \ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \
[red]| |____| |_) | | (__[green]| |  __/>  <| |_ [blue]/ ____ \ (_| |\ V /  __/ | | | |_| |_| | | |  __/
[red]|______| .__/|_|\___[green]|_|\___/_/\_\\__[blue]/_/    \_\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|
[red]       | |                                                                            
[red]       |_|                                                                            
"""

class RollbackManager:
    def __init__(self):
        self.rollbacks: dict[int, str] = {
            0: _TITLE
        }
        self._rollback_level = 0

    def rollback(self):
        clear()
        print(self.rollbacks[self._rollback_level])

    def set_level(self, key: object):
        if key in self.rollbacks.keys():
            self._rollback_level = key

    def add(self, key: object, s: str):
        if key not in self.rollbacks.keys():
            self.rollbacks[key] = s


rollback_manager = RollbackManager()
rollback =  rollback_manager.rollback


class MenuOption:
    def __init__(self, menu_text: str, callback: object, *args, **kwargs):
        self.menu_text = menu_text
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        if self.callback is not None and isinstance(self.callback, Callable):
            return self.callback(*self.args, **self.kwargs)
        else:
            return self.callback

class Menu:
    _MAX_OPTION_PER_PAGE = 9
    _KEY_STYLE = "green"
    _TEXT_STYLE = "white"
    _TITLE_STYLE = "yellow"

    _LEFT_ARROW = "[green]<--"
    _RIGHT_ARROW = "      [green]-->"
    _LEFT_RIGHT_ARROW = "[green]<-- [white]| [green]-->"

    def __init__(self, title: str,
                       menu_options: list[MenuOption],
                       back_option: MenuOption = None,
                       additional: str = None,
                       integrated: bool = False,
                       type_print: bool = False):
        if len(menu_options) == 0:
            self._menu_options = [[]]
        else:
            self._menu_options: list[list[MenuOption]] = \
                [menu_options[i:i + Menu._MAX_OPTION_PER_PAGE] \
                for i in range(0, len(menu_options), Menu._MAX_OPTION_PER_PAGE)]
        self._back_option = back_option
        self._title = title
        self._additional = additional
        self._current_page: int = 0
        self._integrated = integrated
        self._type_print = type_print

    def _has_left(self) -> bool:
        return len(self._menu_options) > 1 and self._current_page != 0
    
    def _has_right(self) -> bool:
        return len(self._menu_options) > 1 and self._current_page != len(self._menu_options) - 1

    def _print_title(self):
        if self._type_print:
            type_print(self._title, style=Menu._TITLE_STYLE)
        else:
            print(self._title, style=Menu._TITLE_STYLE)

    def _print_arrow(self):
        if self._has_left() and self._has_right():
            print(Menu._LEFT_RIGHT_ARROW)
        elif self._has_left():
            print(Menu._LEFT_ARROW)
        elif self._has_right():
            print(Menu._RIGHT_ARROW)

    def _print_page(self):
        if not self._integrated: rollback()
        self._print_title()
        print()
        if self._additional is not None:
            print(self._additional)
            print()
        for i, menu_option in enumerate(self._menu_options[self._current_page]):
            print(str(i + 1), style=Menu._KEY_STYLE, end="")
            print(f" - {menu_option.menu_text}", style=Menu._TEXT_STYLE)
        if self._back_option is not None:
            print()
            print(str(0), style=Menu._KEY_STYLE, end="")
            print(f" - {self._back_option.menu_text}", style=Menu._TEXT_STYLE)
        self._print_arrow()

    def _turn_page_left(self):
        if self._has_left():
            self._current_page -= 1
            rollback()
            self._print_page()

    def _turn_page_right(self):
        if self._has_right():
            self._current_page += 1
            rollback()
            self._print_page()

    @property
    def select(self):
        self._print_page()

        while True:
            key = input_press()
            if key == keyboard.Key.left:
                self._turn_page_left()
            elif key == keyboard.Key.right:
                self._turn_page_right()
            else:
                if hasattr(key, "char"):
                    key_val = key.char
                    if key_val == str(0):
                        return self._back_option
                    for i, menu_option in enumerate(self._menu_options[self._current_page]):
                        if key_val == str(i + 1):
                            return menu_option

print = console.print
input = console.input
clear = console.clear
capture = console.capture
end_capture = console.end_capture
    
def select_from_menu(menu_options: list[MenuOption], max_try: int = -1):
    menu = Menu(menu_options)
    menu.select(max_try)

def input_press():
    with keyboard.Events() as events:
        while True:
            event = events.get()
            if isinstance(event, keyboard.Events.Press):
                break
            time.sleep(0.1)
        return event.key

def input_press_char():
    while True:
        key = input_press()
        if hasattr(key, "char"):
            return key.char

def print_title():
    print(_TITLE)

def scenario_to_string(scenario: Scenario) -> str:
    s = ""
    s += f'[green]{scenario.capital.name}[white], Kingdom of [green]{scenario.kingdom.name}\n'
    s += f'[white]Ruled by: [red]{scenario.ruler.title} {scenario.ruler.name}\n'
    s += f"[white]{scenario.kingdom.description}\n\n"
    s += f"[white]{scenario.ruler.governance_style}\n"
    s += f"[red]{scenario.ruler.evil_deeds}\n\n"
    for region in scenario.kingdom.regions:
        s += f'[white]Region [green]{region.name}\n'
        s += f"[white]{region.description}\n\n"
    return s

def work_with_spinner(work: str, call: Callable, *args, **kwargs):
    spinner = Spinner('aesthetic', work)
    with Live(spinner, refresh_per_second=20) as live:
        return call(*args, **kwargs)

def type_print(text: Text, delay: float = 0.01, style = None):
    for c in text:
        print(c, end='', style=style)
        time.sleep(delay)
    print()


create_figlet_text = pyfiglet.figlet_format

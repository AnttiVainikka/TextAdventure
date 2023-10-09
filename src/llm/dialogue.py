from enum import Enum
from typing import TypedDict

from attr import dataclass

from Characters.character import Character
from llm.connector import connector

@dataclass
class Message:
    speaker: Character
    text: str

    def render(self) -> str:
        return f'{self.speaker.name}: "{self.text}"'

class Dialogue:
    characters: list[Character]
    _messages: list[Message]

    def __init__(self, characters: list[Character]):
        self.characters = characters
        self._messages = []

    def talk_npc(self, character: Character) -> Message:
        msg = Message(character, self.get_npc_reply(character))
        self._messages.append(msg)
        return msg
    
    def talk_player(self, character: Character, msg: str) -> None:
        self._messages.append(Message(character, msg))

    def to_prompt(self) -> str:
        # TODO global text adventure generator/GM prompt
        return f"""You are a text adventure game master.
---
This is a chat between the player character and several NPCs. The characters present are:
{''.join([_character_intro(char) for char in self.characters])}

{"Thus far, the following has been said:" if len(self._messages) > 0 else ''}
{''.join(_render_msg(msg) for msg in self._messages)}
"""
    
    def get_npc_reply(self, character: Character) -> str:
        if len(self._messages) == 0:
            prompt = f"""{self.to_prompt()}

How would the NPC {character.name} initiate this conversation?
Write what they would say below in exactly this format:
<Character name>: "<their reply>"

{'' if connector.chat_model else f'{character.name}:'}"""
        else:
            prompt = f"""{self.to_prompt()}

How would the NPC {character.name} reply to this?
Write their reply below in this format:
<Character name>: "<their reply>"

{'' if connector.chat_model else f'{character.name}:'}"""
        result = connector.complete(prompt, {
            'temperature': 1.0,
            'stop_sequences': ['\n']
        })[0]
        start = result.find('"')
        end = result.find('"', start + 1)
        return result[start + 1:end]

def _character_intro(char: Character) -> str:
    return f"""- {char.name} ({'NPC' if char.kind == 'npc' else 'player character'})
{char.description}
"""

def _render_msg(message: Message) -> str:
    return f'{message.render()}\n\n'
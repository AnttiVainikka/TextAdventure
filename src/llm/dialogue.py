import os
from typing import Optional

from attr import dataclass

from Characters.character import Character
from llm.connector import OpenAIConnector, connector
from llm.error import GenerateFailure

if os.environ.get('DIALOGUE_GPT4') == 'true':
    # Quick hack to use GPT-4 only for dialogue
    connector = OpenAIConnector('gpt-4-1106-preview', chat_model=True)

@dataclass
class Message:
    speaker: Optional[Character]
    mannerisms: str
    text: str

    def render(self) -> str:
        if self.speaker == None:
            return self.text
        elif self.speaker.kind == 'npc':
            return f'{self.mannerisms} "{self.text}"'
        else:
            return f'{self.speaker.name}: "{self.text}"'

class Dialogue:
    context: str
    characters: list[Character]
    _messages: list[Message]

    def __init__(self, context: str, characters: list[Character]):
        self.context = context
        self.characters = characters
        self._messages = []
        #self._who_next = Question('Which NPC character should speak next?', [character.name for character in characters if character.kind == 'npc'])

    def talk_npc(self, character: Optional[Character] = None, instruction: Optional[str] = None) -> Message:
        # if character == None:
        #     character = self._next_speaker()
        msg = self._get_npc_reply(character, instruction)
        self._messages.append(msg)
        return msg
    
    def talk_player(self, character: Character, msg: str) -> None:
        self._messages.append(Message(character, '', msg))

    def add_note(self, note: str) -> None:
        self._messages.append(Message(None, '', note))

    def analyze(self, question: str) -> str:
        prompt = f"""{self._to_prompt()}

{question}"""
        return connector.complete(prompt, {
            'temperature': 1.0,
            'stop_sequences': ['\n']
        })[0]

    def _to_prompt(self) -> str:
        return f"""You are a text adventure game master.
---
{self.context}

The characters present are:
{''.join([_character_intro(char) for char in self.characters])}

{"Thus far, these things have been said:" if len(self._messages) > 0 else ''}
{''.join(_render_msg(msg) for msg in self._messages)}"""
    
    def _get_npc_reply(self, character: Optional[Character], instruction: Optional[str] = 'Be brief; this is spoken dialogue.') -> Message:
        for _ in range(2):
            
            if len(self._messages) == 0:
                prompt = f"""{self._to_prompt()}

{'How would one of the NPCs (not the player character) begin the conversation?'
 if character == None else f'How would the NPC {character.name} initiate this conversation?'}
{instruction}
Write what they would say below in exactly this format:
<Character name> <character mannerisms>. "<their reply>"
"""
            else:
                prompt = f"""{self._to_prompt()}

{'How would one of the NPCs continue this conversation?'
 if character == None else 'How would the NPC {character.name} reply to this?'}
{instruction}
Write their reply below in this format:
<Character name> <character mannerisms>. "<their reply>"
"""

            result = connector.complete(prompt, {
                'temperature': 1.0,
                'stop_sequences': ['\n']
            })[0]

            quote_start = result.find('"')
            if quote_start == -1:
                continue
            quote_end = result.find('"', quote_start + 1)
            if quote_end < len(result) - 5:
                continue # LLM propably tried to generate something after this
            
            mannerisms = result[:quote_start]
            if character == None:
                for ch in [ch for ch in self.characters if ch.kind == 'npc']:
                    if ch.name.lower() in mannerisms.lower():
                        character = ch
                        break
            if character == None:
                raise GenerateFailure(f'_next_speaker: no NPC name found in "{mannerisms}"')

            return Message(character, mannerisms, result[quote_start + 1:quote_end])
        raise GenerateFailure(f'dialogue generation failed')


def _character_intro(char: Character) -> str:
    return f"""- {char.name} ({'NPC' if char.kind == 'npc' else 'player character'})
{char.description}
"""

def _render_msg(message: Message) -> str:
    if message.speaker == None:
        return message.text + '\n'
    else:
        return f'{message.speaker.name}: "{message.text}"\n'
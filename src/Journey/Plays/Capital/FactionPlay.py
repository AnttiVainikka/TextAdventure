from typing import TYPE_CHECKING, Optional
from Generation.faction import Faction
from Generation.npc import Character
from Generation.scenario import Scenario

from Journey.Plays.Play import Play
from Journey.Interaction import Interaction

from Journey.Action import InteractionAnsweredAction, PlayFinishedAction
from llm.dialogue import Dialogue

if TYPE_CHECKING:
    from Journey.Scenes.CapitalScene import CapitalScene

class FactionPlay(Play):
    _player: Character
    _faction: Faction
    _chat: Dialogue

    _turns_left: int
    _prev_interaction: Optional[Interaction]
    favor: int

    def __init__(self, parent: "CapitalScene", player: Character, scenario: Scenario, faction: Faction):
        super().__init__(parent)
        self._player = player
        self._faction = faction
        self._chat = _init_dialogue(player, scenario, faction)
        self._turns_left = 10
        self._prev_interaction = None
        self.favor = faction.favor

    def has_next(self):
        return self._turns_left > 0

    def reset(self):
        raise RuntimeError('unimplemented')

    def _next(self) -> Interaction:
        if self._prev_interaction != None:
            # Append player's reply to dialogue thread and analyze the sentiment in it
            self._chat.talk_player(self._player, self._prev_interaction.answer)
            sentiment = self._chat.analyze(_SENTIMENT_PROMPT).lower()

            # Based on sentiment, change favor
            # If it crosses a threshold, also explicitly add a note about this to chat history
            old_favor_text = _get_favor_text(self.favor)
            match sentiment:
                case 'positive':
                    self.favor += 5
                    self._chat.add_note(f'{self._faction.name} approves of this.')
                case 'negative':
                    self.favor -= 5
                    self._chat.add_note(f'{self._faction.name} did not appreciate that.')
            new_favor_text = _get_favor_text(self.favor)
            if old_favor_text != new_favor_text:
                self._chat.add_note(f'{self._faction.name} is now {_get_favor_text(self.favor)}')

        self._turns_left -= 1
        # TODO raise_action
        if self.favor <= -50:
            self._chat.add_note(f'{self._faction.name} will now ATTACK the player!')
            print(self._chat.talk_npc().render())
            return None
        elif self.favor >= 50:
            self._chat.add_note(f'The player character has convinced {self._faction.name} to join the rebellion! They have received all they want from the player character.')
            print(self._chat.talk_npc(instruction='The faction leader should tell the player character that they will join the rebellion.').render())
            return None
        elif self._turns_left == 0:
            self._chat.add_note(f'{self._faction.name} is still {_get_favor_text(self.favor)}')
            self._chat.add_note('Their members are no longer interested in continuing this conversation.')
            print(self._chat.talk_npc().render())
            return None

        # Let one of the NPCs talk
        msg = self._chat.talk_npc()
        interaction = Interaction(self, msg.render())
        self._prev_interaction = interaction
        return interaction

_SENTIMENT_PROMPT = """Analyze the sentiment of the player character's latest response.

Classify it as one of: positive, negative, neutral
Reply ONLY with the one of these three words!"""

def _get_favor_text(favor: str) -> str:
    if favor >= 25:
        return 'already quite ready to support the rebellion. Its members will be friendly.'
    elif favor >= 0:
        return 'currently neutral and would probably join the rebellion if for a good reason. Its members will be polite, but not necessarily friendly.'
    elif favor >= -25:
        return 'unwilling to rebel for its own reasons. Its members will make their dislike known, but will not resort to violence.'
    else:
        return 'fiercely loyal to the current ruler. Its members will be outright hostile, with words if not swords.'
    
def _init_dialogue(player: Character, scenario: Scenario, faction: Faction) -> Dialogue:
    # Create context with basic world information, etc.
    context = f"""{scenario.kingdom.description}

{scenario.ruler.evil_deeds} {scenario.ruler.personality}

{scenario.ruler.governance_style} {scenario.ruler.evil_deeds}

But now, a rebellion to overthrow the {scenario.ruler.title} {scenario.ruler.name} is brewing. The rebel leader {player.name} is looking for allies.

{faction.overview} {faction.beliefs} {faction.goals} {faction.needs} {faction.name} is {faction.alignment.value}.

{player.name} has come to discuss something with them. They do not yet know why this is the case, but they do know tha {player.name} is suspected to be a rebel.

{faction.name} is initially {_get_favor_text(faction.favor)}
This the conversation between {player.name} and several of leaders of the faction."""
    
    # Convert NPCs to game characters TODO memoize for performance
    npcs = [npc.game_character() for npc in faction.npcs]
    return Dialogue(context, [player, *npcs])
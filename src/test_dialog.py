import random
import sys
from Characters.character import Character
from llm.dialogue import Dialogue
from world import load_world

def get_favor_text(favor: str) -> str:
    if favor >= 25:
        return 'already quite ready to support the rebellion. Its members will be friendly.'
    elif favor >= 0:
        return 'currently neutral and would probably join the rebellion if for a good reason. Its members will be polite, but not necessarily friendly.'
    elif favor >= -25:
        return 'unwilling to rebel for its own reasons. Its members will make their dislike known, but will not resort to violence.'
    else:
        return 'fiercely loyal to the current ruler. Its members will be outright hostile, with words if not swords.'

world = load_world(sys.argv[1])

print('Select a faction:')
for i, faction in enumerate(world.factions):
    print(f'{i}. {faction.name} ({faction.alignment.name}, favor: {faction.favor})')

faction = world.factions[int(input('Faction: '))]

player = Character('pc', 'Ina', {}, 1, "Ina is the hero of an rebellion soon to come.")

scenario = world.scenario
context = f"""{scenario.kingdom.description}

{scenario.ruler.evil_deeds} {scenario.ruler.personality}

{scenario.ruler.governance_style} {scenario.ruler.evil_deeds}

But now, a rebellion to overthrow the {scenario.ruler.title} {scenario.ruler.name} is brewing. The rebel leader {player.name} is looking for allies.

{faction.overview} {faction.beliefs} {faction.goals} {faction.needs} {faction.name} is {faction.alignment.value}.

{player.name} has come to discuss something with them. They do not yet know why this is the case, but they do know tha ${player.name} is suspected to be a rebel.

${faction.overview} is initially ${get_favor_text(faction.favor)}
This the conversation between {player.name} and several of leaders of the faction."""
npcs = [npc.game_character() for npc in faction.npcs]
chat = Dialogue(context, [player, *npcs])
print(chat.talk_npc().render())

SENTIMENT_PROMPT = """Analyze the sentiment of the player character's latest response.

Classify it as one of: positive, negative, neutral
Reply ONLY with the one of these three words!"""

while True:
    reply = input('Ina (you): ')
    chat.talk_player(player, reply)
    sentiment = chat.analyze(SENTIMENT_PROMPT).lower()
    match sentiment:
        case 'positive':
            chat.add_note(f'${faction.name} approves of this.')
        case 'negative':
            chat.add_note(f'${faction.name} did not appreciate that.')
    print(sentiment)
    print(chat.talk_npc().render())

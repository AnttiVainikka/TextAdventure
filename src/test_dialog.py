import random
import sys
from Characters.character import Character
from llm.dialogue import Dialogue
from world import load_world


world = load_world(sys.argv[1])

print('Select a faction:')
for i, faction in enumerate(world.factions):
    print(f'{i}. {faction.name} ({faction.alignment.name}, favor: {faction.favor})')

faction = world.factions[int(input('Faction: '))]
if faction.favor > 50:
    stance = 'are already willing to support the rebellion, so this should be easy'
elif faction.favor > 25:
    stance = 'are tentatively interested in joining a rebellion, with a little persuasion'
elif faction.favor > 0:
    stance = 'might be willing to join a rebellion if it advances their goals'
elif faction.favor > -25:
    stance = 'have their own reasons to avoid rebelling, but might be willing to listen to a right person'
else:
    stance = 'are loyal to the current ruler, so this is rather risky move'

player = Character('pc', 'Ina', {}, 1, "Ina is the hero of an rebellion soon to come.")

scenario = world.scenario
context = f"""{scenario.kingdom.description}

{scenario.ruler.evil_deeds} {scenario.ruler.personality}

{scenario.ruler.governance_style} {scenario.ruler.evil_deeds}

But now, a rebellion to overthrow the {scenario.ruler.title} {scenario.ruler.name} is brewing. The rebel leader {player.name} is looking for allies.

{faction.overview} {faction.beliefs} {faction.goals} {faction.needs} {faction.name} is {faction.alignment.value}.

{player.name} has come to try to recruit them. They {stance}. This the conversation between {player.name} and members of {faction.name}."""
npcs = [npc.game_character() for npc in faction.npcs]
chat = Dialogue(context, [player, *npcs])
print(chat.talk_npc().render())

while True:
    reply = input('Ina (you): ')
    chat.talk_player(player, reply)
    print(chat.talk_npc().render())
    joined_rebels = chat.analyze('Have the player character and the faction agreed on terms of joining the rebellion? Reply with yes or no, nothing else.')
    if 'yes' in joined_rebels.lower():
        print(f'Congratulations! {faction.name} has joined the rebellion!')
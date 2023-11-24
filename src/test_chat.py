import sys
from Characters.character import Character
from Journey.Plays.Capital.FactionPlay import FactionPlay
from world import load_world

world = load_world(sys.argv[1])

print('Select a faction:')
for i, faction in enumerate(world.factions):
    print(f'{i}. {faction.name} ({faction.alignment.name}, favor: {faction.favor})')

faction = world.factions[int(input('Faction: '))]

player = Character('pc', 'Ina', {}, 1, "Ina is the hero of an rebellion soon to come.")


faction_play = FactionPlay(None, player, world.scenario, faction)
while faction_play.has_next():
    interaction = faction_play.next()
    if interaction == None:
        break
    print(interaction)
    interaction(input("Ina (you): "))
    print(f'favor: {faction_play.favor}')

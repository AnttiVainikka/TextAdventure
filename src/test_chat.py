from Journey.Plays.Capital.FactionPlay import FactionPlay

faction_play = FactionPlay(None, None)
while faction_play.has_next():
    interaction = faction_play.next()
    print(interaction)
    if interaction.is_info:
        interaction("")
    else:
        interaction(input())

import random
from Characters.character import Character
from llm.dialogue import Dialogue


mercenary_boss = Character('npc', 'Ral', {}, 1, "Ral is a ruthless mercenary captain, who will do anything to win. What he won't do, is unnecessarily risk lives of his subordinates.")
mercenary_a = Character('npc', 'Myn', {}, 1, "Myn is Ral's right hand. She takes care of actually leading the mercenaries on the battlefield.")
mercenary_b = Character('npc', 'Sova', {}, 1, "Sova joined the mercenaries a while ago, and has already gained notoriety by his ruthlessness and prowess in battle.")

player = Character('pc', 'Ina', {}, 1, "Una is the hero of an rebellion soon to come. They are not a mercenary, though.")

chat = Dialogue([mercenary_boss, mercenary_a, mercenary_b, player])
print(chat.talk_npc(mercenary_boss).render())

npcs = [mercenary_boss, mercenary_a, mercenary_b]
while True:
    reply = input('Ina (you): ')
    chat.talk_player(player, reply)
    npc = npcs[random.randint(0, len(npcs) - 1)]
    print(chat.talk_npc(npc).render())

from Characters.create import create_enemies
from battle import battle

player_party = create_enemies(25,8)
for i in range(5,9):
    level = player_party[0].level
    enemy_party = create_enemies(level,i)
    if battle(player_party,enemy_party) != "victory":
        print("Better luck next time")
        break
    else:
        print(f"You have defeated difficulty {i}. {8-i} battles remain")

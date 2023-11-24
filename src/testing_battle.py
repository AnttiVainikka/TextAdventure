from Characters.create import create_enemies
from Generation.enemy_type import EnemyType, EnemyRarity
from battle import battle

test_enemy_type = [EnemyType("Goblin", "Jeff", "Nasty lookign goblin", EnemyRarity.Legendary)]

player_party = create_enemies(25,8,test_enemy_type)
for i in range(5,9):
    level = player_party[0].level
    enemy_party = create_enemies(level,i, test_enemy_type)
    if battle(player_party,enemy_party) != "victory":
        print("Better luck next time")
        break
    else:
        print(f"You have defeated difficulty {i}. {8-i} battles remain")

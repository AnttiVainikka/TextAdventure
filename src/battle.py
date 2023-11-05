from random import randint
from time import sleep
def battle(players :list,enemies :list):
    """
    players: list consisting of player character and possible allies
    enemies: list of enemies

    Returns:
    "victory" if battle is won
    "defeat" if battle is lost
    "run" if player wishes to try to run away
    """
    dead_enemies = 0
    dead_players = 0
    while True: #Loop that breaks when all enemies or players are dead
        #Ask the player to take action with each ally character
        for player in players:
            sleep(1)
            if len(enemies) - dead_enemies <= 0:
                for enemy in enemies:
                    for player in players:
                        if player.alive:
                            player.gain_exp(enemy.given_exp)
                return "victory"
            if player.alive:
                #Print the names, level and hp of all combatants at the start of every turn
                print("\nYour Party")
                for p in players:
                    print(f"{p.name} LVL {p.level}:  HP: {p.stats['hp']}/{p.stats['hp']+p.lost_hp}")
                print("\nEnemy Party")
                for e in enemies:
                    print(f"{e.name}: LVL {e.level}  HP: {e.stats['hp']}/{e.stats['hp']+e.lost_hp}")
                print("\n")
                while True: #breaks once player does an action successfully
                    print("Attack:  1\nSkill:  2\nRun:  3\n")
                    #use item can be implemented later if we want
                    action = input(f"Choose action for {player.name}:  ")
                    while action not in ["1","2","3"]:
                        action = input("Please type 1, 2 or 3:  ")
                    if action == "3":
                        for enemy in enemies:
                            for player in players:
                                if player.alive:
                                    if not enemy.alive:
                                        player.gain_exp(enemy.given_exp)
                        return "run"
                        #let the llm decide if it succeeds, if llm is bad at it random chance can be implemented
                        #there is an exploit if you have many party members to attack with others and run with the
                        #last one since players always start the battle assuming the battle will continue as it was

                    elif action == "2": # Everything under this elif could be put to its own function since it's quite long
                        #Print the characters skills and prompt the player to choose one
                        counter = 1
                        print("\n")
                        for skill in player.skills:
                            print(f"{counter}:  {skill.name}  Uses {skill.uses_remaining}/{skill.uses}")
                            counter += 1
                        print(f"{counter}:  Back")
                        try:
                            while True:
                                skill = int(input("Choose skill:  "))
                                if skill not in range(1,counter+1):
                                    print("Invalid choice")
                                else:
                                    break
                        except ValueError:
                            print("Invalid input\n")
                            continue
                        if skill == counter: #back was chosen
                            continue
                        skill = player.skills[skill-1]
                        if skill.uses_remaining <= 0:
                            print("Selected skill has no uses left")
                            continue
                        if skill.ally:
                            # currently only healing skills work for self targeting skills
                            # various buffing skills can be implemented later if we wish
                            if skill.stat == "atk":
                                heal = int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier)
                            else:
                                heal = int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier)
                            if skill.aoe or len(players)-dead_players <= 1:
                                for player in players:
                                    if player.alive:
                                        player.take_damage(heal)
                                        print(f"{player.name} was healed for {-heal}")
                            else:
                                # Promt player to select which character to heal
                                counter = 1
                                print("\n")
                                for p in players:
                                    print(f"{p.name} HP:{p.stats['hp']}/{p.stats['hp']+p.lost_hp}:  {counter}")
                                    counter += 1
                                print(f"Back:  {counter}")
                                try:
                                    while True:
                                        target = int(input("Choose target:  "))
                                        if target not in range(1,counter+1):
                                            print("Invalid target")
                                        else:
                                            break
                                except ValueError:
                                    print("Invalid input\n")
                                    continue
                                if target == counter: #back was chosen
                                    continue
                                target = players[target-1]
                                if target.alive:
                                    target.take_damage(heal)
                                    print(f"{target.name} was healed for {-heal}")
                                else:
                                    print("Fallen characters cannot be healed")
                                    continue
                        else: #skill is a damaging skill
                            #currently only damaging skills work, debuffs can be implemented later
                            if skill.aoe or len(enemies)-dead_enemies <= 1:
                                for enemy in enemies:
                                    if enemy.alive:
                                        if skill.stat == "atk":
                                            damage = max(1,int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier-enemy.armour.stats[0]))
                                        else:
                                            damage = max(1,int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier-enemy.armour.stats[1]))
                                        if enemy.take_damage(damage) == "dead":
                                            print(f"{enemy.name} took {damage} damage and was defeated")
                                            dead_enemies += 1
                                        else:
                                            print(f"{enemy.name} took {damage} damage")
                            else: # Skill is single target
                                # Promt player to select which enemy to attack
                                counter = 1
                                print("\n")
                                for enemy in enemies:
                                    print(f"{enemy.name} HP:{enemy.stats['hp']}/{enemy.stats['hp']+enemy.lost_hp}:  {counter}")
                                    counter += 1
                                print(f"Back:  {counter}")
                                try:
                                    while True:
                                        target = int(input("Choose target:  "))
                                        if target not in range(1,counter+1):
                                            print("Invalid target")
                                        else:
                                            break
                                except ValueError:
                                    print("Invalid input\n")
                                    continue
                                if target == counter: #back was chosen
                                    continue
                                target = enemies[target-1]
                                if target.alive:
                                    if skill.stat == "atk":
                                        damage = max(1,int((player.stats["atk"]+player.weapon.stats[0])*skill.multiplier-target.armour.stats[0]))
                                    else:
                                        damage = max(1,int((player.stats["magic"]+player.weapon.stats[1])*skill.multiplier-target.armour.stats[1]))
                                    if target.take_damage(damage) == "dead":
                                        print(f"{target.name} took {damage} damage and was defeated")
                                        dead_enemies += 1
                                    else:
                                        print(f"{target.name} took {damage} damage")
                                else:
                                    print("Fallen enemies cannot be attacked")
                                    continue
                        skill.uses_remaining -= 1
                        break #getting to this line should mean a skill has been successfully used
                    else: # action is "3" as in a normal attack
                        counter = 1
                        print("\n")
                        for enemy in enemies:
                            print(f"{enemy.name} HP:{enemy.stats['hp']}/{enemy.stats['hp']+enemy.lost_hp}:  {counter}")
                            counter += 1
                        print(f"Back:  {counter}")
                        try:
                            while True:
                                target = int(input("Choose target:  "))
                                if target not in range(1,counter+1):
                                    print("Invalid target")
                                else:
                                    break
                        except ValueError:
                            print("Invalid input\n")
                            continue
                        if target == counter: #back was chosen
                            continue
                        target = enemies[target-1]
                        if target.alive:
                            damage = max(1,int(player.stats["atk"]+player.weapon.stats[0]-target.armour.stats[0]))
                            if target.take_damage(damage) == "dead":
                                print(f"{target.name} took {damage} damage and was defeated")
                                dead_enemies += 1
                            else:
                                print(f"{target.name} took {damage} damage")
                        else:
                            print("Fallen enemies cannot be attacked")
                            continue
                        break #Enemy was successfully attacked
        for enemy in enemies:
            #TODO There should probably be some testing for enemy skill usage, though it's hard to test in battle
            if enemy.alive:
                sleep(1)
                # Randomly decide target
                counter = 0
                valid_targets = []
                for p in players:
                    if p.alive:
                        valid_targets.append(counter)
                    counter += 1
                if len(valid_targets) == 0:
                    return "defeat"
                target = players[valid_targets[randint(0,len(valid_targets)-1)]]
                # Check if there is an enemy with low hp to heal
                enemy_to_heal = False
                counter = 0
                for e in enemies:
                    if e.lost_hp >= e.stats["hp"]/2 and e.alive:
                        enemy_to_heal = enemies[counter]
                    counter += 1
                # Check if there are skills to use
                skill_to_use = False
                counter = 0
                for skill in enemy.skills:
                    if skill.uses_remaining > 0:
                        if skill.multiplier < 0:
                            if enemy_to_heal:
                                skill_to_use = counter
                        else:
                            skill_to_use = counter
                    counter += 1
                # Decide if to use skill with 1 in 3 chance
                if skill_to_use:
                    if randint(1,3) == 3:
                        skill = enemy.skills[skill_to_use]
                        if skill.stat == "atk":
                            damage = int((enemy.stats["atk"]+enemy.weapon.stats[0])*skill.multiplier)
                        else:
                            damage = int((enemy.stats["magic"]+enemy.weapon.stats[1])*skill.multiplier)
                        if skill.multiplier < 0:
                            if skill.aoe:
                                for e in enemies:
                                    if e.alive:
                                        e.take_damage(damage)
                                        print(f"{e.name} was healed for {-damage}")
                            else:
                                enemy_to_heal.take_damage(damage)
                                print(f"{enemy_to_heal.name} was healed for {-damage}")
                        else:
                            if skill.stat == "atk":
                                damage = max(1,damage-target.armour.stats[0])
                            else:
                                damage = max(1,damage-target.armour.stats[1])
                            if target.take_damage(damage) == "dead":
                                print(f"{target.name} took {damage} damage and was defeated")
                                dead_players += 1
                            else:
                                print(f"{target.name} took {damage} damage")
                        if len(players) - dead_players <= 0:
                            return "defeat"
                        skill.uses_remaining -= 1
                        continue #ends turn for current enemy after successful skill usage
                damage = max(1,int(enemy.stats["atk"]+enemy.weapon.stats[0]-target.armour.stats[0]))                 
                if target.take_damage(damage) == "dead":
                    print(f"{target.name} took {damage} damage and was defeated")
                    dead_players += 1
                else:
                    print(f"{target.name} took {damage} damage")
                if len(players) - dead_players <= 0:
                    return "defeat"

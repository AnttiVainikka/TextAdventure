# Idea for a battle system from Antti:

# Eventually characters can be given speed stats but for now
# we could give the player and the enemy alternating turns.
# Let the player use a turn to attack the enemy, use a skill, try to run,
# or start talking to the enemy. For running and talking we can let
# the LLM decide what happens (or implement speed/speech stat) but for 
# attacking we can have Python calculate the damage like this:
p = "attacker"
e = "attacked"
skill = ""
if e.armour != None:
    #normal attack
    damage = max(1,p.stats["atk"][p.level]+p.weapon.stats[0] - e.armour.stats[0])
    #physical skill
    damage = max(1,(p.stats["atk"][p.level]+p.weapon.stats[0])*skill.multiplier - e.armour.stats[0])
    #magic skill
    damage = max(1,(p.stats["magic"][p.level]+p.weapon.stats[1])*skill.multiplier - e.armour.stats[1])
else:
    pass
    # skip the armour part 
e.stats["hp"][e.level] -= damage

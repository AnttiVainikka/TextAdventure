from Characters.create import create_skill

def printSkill(skill):
    print(f"""Spell: {skill.name}
Description: {skill.description}
stat: {skill.stat}
uses: {skill.uses}
uses_remaining: {skill.uses_remaining}
ally: {skill.ally}
aoe: {skill.aoe}
""")

skill = create_skill("warrior", 3)
printSkill(skill)

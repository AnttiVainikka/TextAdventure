class Equipment():
    def __init__(self, type :str, stats :list, description :str):
        """
        type: weapon/armour
        (more variety to armour pieces can be added later (gloves, boots...))
        stats: [physical damage/armour, magical damage/armour]
        description: for LLM to use when describing the equipment
        """
        self.type = type
        self.stats = stats
        self.description = description
        self.durability = 100 # Do we want them to break eventually?

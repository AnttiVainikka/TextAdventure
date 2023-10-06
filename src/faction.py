class Faction():
  def __init__(self, name :str, description :str, location :str, setting :str, reward):
    self.name = name
    self.description = description
    self.power = None # Might be implemented later
    self.location = location
    self.setting = setting
    self.leader = None
    self.hostility=0 # -100 is min and 100 max
    self.reward = reward

  def __str__(self): # It would be beneficial to have the reward maybe displayed in a more intricate manner
    return f"Faction name: {self.name} \n" \
          f"Faction description: {self.description} \n" \
          f"Faction Location: {self.location} \n" \
          f"Faction setting: {self.setting} \n" \
          f"Faction reward: {self.reward.description} \n" \
          f"Faction hostility: {self.hostility}"

  def alter_hostility(self, value):
    self.hostility += value
    if (self.hostility > 100):
      self.hostility = 100
    if (self.hostility < -100):
      self.hostility = -100
    

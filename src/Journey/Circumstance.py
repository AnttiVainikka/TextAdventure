
class Circumstance:
    def __init__(self, circumstance: str = ""):
        self._intuition = circumstance

    @property
    def circumstance(self):
        return self._intuition
    
    @circumstance.setter
    def circumstance(self, circumstance: str):
        self._intuition = circumstance

    def __str__(self):
        return self._intuition
    
class Circumstances:
    def __init__(self, circumstances: list[Circumstance] = []):
        self._intuitions = circumstances

    @property
    def circumstances(self):
        return self._intuitions
    
    @circumstances.setter
    def circumstances(self, circumstances: list[Circumstance]):
        self._intuitions = circumstances

    def add(self, circumstance: Circumstance):
        self._intuitions.append(circumstance)

    def __len__(self):
        return len(self._intuitions)
    
    def __str__(self):
        return '\n'.join(str(circumstance) for circumstance in self._intuitions)

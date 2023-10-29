
class Intuition:
    def __init__(self, intuition: str = ""):
        self._intuition = intuition

    @property
    def intuition(self):
        return self._intuition
    
    @intuition.setter
    def intuition(self, intuition: str):
        self._intuition = intuition

    def __str__(self):
        return self._intuition
    
class Intuitions:
    def __init__(self, intuitions: list[Intuition] = []):
        self._intuitions = intuitions

    @property
    def intuitions(self):
        return self._intuitions
    
    @intuitions.setter
    def intuitions(self, intuitions: list[Intuition]):
        self._intuitions = intuitions

    def add(self, intuition: Intuition):
        self._intuitions.append(intuition)

    def __len__(self):
        return len(self._intuitions)
    
    def __str__(self):
        return '\n'.join(str(intuition) for intuition in self._intuitions)

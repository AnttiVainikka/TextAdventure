import numpy as np

class Selector:
    def __init__(self, values: list[object], probabilities: list[float]):
        self._values = np.array(values)
        self._probabilities = np.array(probabilities)
        self._probabilities /= sum(probabilities) # normalize

    def __call__(self) -> object:
        return self._values[self._select_index()]
    
    def _select_index(self) -> int:
        return np.random.choice([*range(0, len(self._values))], 1, p=self._probabilities)[0]

class NonRepSelector(Selector):
    def __init__(self, values: list[object], probabilities: list[float], l:float):
        super().__init__(values, probabilities)
        self._default_probabilities = np.array(probabilities)
        self._l = l

    def __call__(self) -> object:
        index = self._select_index()
        if len(self._values) > 1:
            self._update(index)
        return self._values[index]

    def _update(self, index: int):
        temp_probabilities = self._default_probabilities.copy()
        temp_probabilities[index] = 0.0
        temp_probabilities /= np.sum(temp_probabilities)

        split_value = self._probabilities[index] * (1.0 - self._l)
        self._probabilities[index] *= self._l

        for i in range(0, len(temp_probabilities)):
            self._probabilities[i] += split_value * temp_probabilities[i]

        if index != 0:
            self._probabilities[0] = 1.0 - sum(self._probabilities[1:])
        else:
            self._probabilities[-1] = 1.0 - sum(self._probabilities[:-1])
        
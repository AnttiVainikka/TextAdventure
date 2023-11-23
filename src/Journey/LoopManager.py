from abc import ABC, abstractmethod

class LoopManager(ABC):
    def __init__(self):
        self._in_progress = False
        self._first_start = True

    def run(self):
        if self._first_start:
            self._start()
            self._first_start = False
        else:
            self._restart()

        self._in_progress = True
        while self._in_progress:
            self._do_work()

        self._end()

    @property
    def in_progress(self) -> bool:
        return self._in_progress

    def stop(self):
        self._in_progress = False

    def _start(self):
        pass

    def _restart(self):
        pass

    def _end(self):
        pass

    @abstractmethod
    def _do_work(self):
        pass

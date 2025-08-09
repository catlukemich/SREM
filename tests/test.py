import abc

class Test:
    def __init__(self, main):
        self.main = main

    @abc.abstractmethod
    def update(self, main, clock):
        pass

    @abc.abstractmethod
    def on_event(self):
        pass
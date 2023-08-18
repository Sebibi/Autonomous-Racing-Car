from abc import ABC, abstractmethod


class PygameObject(ABC):

    @abstractmethod
    def draw(self, screen):
        pass
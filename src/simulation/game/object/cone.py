import pygame

from src.simulation.game.object.base import PygameObject


class Cone(PygameObject):
    size = 10

    def __init__(self, x: int, y: int, color: pygame.Color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.polygon(
            surface=screen,
            color=self.color,
            points=[(self.x, self.y - self.size),
                    (self.x - self.size, self.y + self.size),
                    (self.x + self.size, self.y + self.size)])

    def get_position(self):
        return self.x, self.y

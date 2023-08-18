import pygame
from pygame.colordict import THECOLORS

from src.simulation.game.object.cone import Cone
from src.simulation.track.base import TrackBase


class ConeTrackBase(TrackBase):
    inner_cones: list[Cone]
    outer_cones: list[Cone]
    center_line: list[tuple[int, int]]
    start_position = tuple[int, int]
    inner_limit: pygame.Rect
    outer_limit: pygame.Rect

    def __init__(self, screen: pygame.Surface,
                 inner_track: list[tuple[int, int]],
                 outer_track: list[tuple[int, int]],
                 middle_track: list[tuple[int, int]],
                 starting_position: tuple[int, int, int] | list[int]):
        self.inner_cones = [Cone(cone[0], cone[1], THECOLORS['yellow']) for cone in inner_track]
        self.outer_cones = [Cone(cone[0], cone[1], THECOLORS['blue']) for cone in outer_track]
        self.center_line = middle_track
        self.start_position = starting_position
        super().__init__(screen)

    def draw(self):
        inner_coords = [cone.get_position() for cone in self.inner_cones]
        outer_coords = [cone.get_position() for cone in self.outer_cones]
        pygame.draw.polygon(self.screen, THECOLORS['black'], outer_coords, 0)
        pygame.draw.polygon(self.screen, THECOLORS['white'], inner_coords, 0)

        for cone in self.inner_cones:
            cone.draw(self.screen)

        for cone in self.outer_cones:
            cone.draw(self.screen)

    def get_start_position(self):
        return self.start_position

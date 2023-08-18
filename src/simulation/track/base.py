from abc import ABC, abstractmethod

import pygame
from pygame.colordict import THECOLORS


def draw_cones(screen, cone_positions: list, color: tuple[int, int, int]):
    for cone_pos in cone_positions:
        pygame.draw.polygon(screen, color, [(cone_pos[0], cone_pos[1] - 10),
                                            (cone_pos[0] - 10, cone_pos[1] + 10),
                                            (cone_pos[0] + 10, cone_pos[1] + 10)])


class TrackBase(ABC):

    game_map: pygame.Surface

    def __init__(self, game_map: pygame.Surface):
        self.game_map = game_map

    @abstractmethod
    def draw(self, screen: pygame.Surface, car_position: tuple[int, int]):
        pass

    def in_track_limit(self, rect: pygame.Rect | tuple):
        white = THECOLORS['white']
        try:
            if isinstance(rect, tuple):
                return self.game_map.get_at(rect) != white
            is_not_black = self.game_map.get_at(rect.topleft) != white \
                           and self.game_map.get_at(rect.topright) != white \
                           and self.game_map.get_at(rect.bottomleft) != white \
                           and self.game_map.get_at(rect.bottomright) != white
        except IndexError:
            return False
        return is_not_black

    @abstractmethod
    def get_start_position(self):
        pass










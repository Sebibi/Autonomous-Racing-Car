from abc import ABC, abstractmethod

import numpy as np
import pygame
from pygame.colordict import THECOLORS


def draw_cones(screen, cone_positions: list, color: tuple[int, int, int]):
    for cone_pos in cone_positions:
        pygame.draw.polygon(screen, color, [(cone_pos[0], cone_pos[1] - 10),
                                            (cone_pos[0] - 10, cone_pos[1] + 10),
                                            (cone_pos[0] + 10, cone_pos[1] + 10)])


class TrackBase(ABC):

    game_map: pygame.Surface
    center_line: np.ndarray

    def __init__(self, game_map: pygame.Surface, center_line: np.ndarray):
        self.game_map = game_map
        self.center_line = center_line

    def draw(self, screen: pygame.Surface, car_position: tuple[int, int]):
        # x = screen.get_width() // 2 - car_position[0]
        # y = screen.get_height() // 2 - car_position[1]
        screen.fill(THECOLORS["white"])
        screen.blit(self.game_map, dest=(0, 0))

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

    def get_center_line_index(self, point: np.ndarray, previous_index: int = None) -> tuple[int, float]:
        if previous_index is not None:
            search_slice = (np.arange(15) - 4 + previous_index) % len(self.center_line)
            center_line = self.center_line[search_slice]
            distances = np.linalg.norm(center_line - point, axis=1)
            local_arg_min = np.argmin(distances)
            local_arg_mins = np.array([local_arg_min - 1, local_arg_min, local_arg_min + 1]) % len(center_line)
            distance: float = np.mean(distances[local_arg_mins])
            arg_min: int = (local_arg_min + search_slice[0]) % len(self.center_line)
            return arg_min, distance
        else:
            center_line = self.center_line
            distances = np.linalg.norm(center_line - point, axis=1)
            arg_min: int = np.argmin(distances)
            arg_mins = np.array([arg_min - 1, arg_min, arg_min + 1]) % len(center_line)
            distance: float = np.mean(distances[arg_mins])
            return arg_min, distance

    def get_center_line_in_front(self, car_position: tuple[int, int] = None,
                                 center_line_index: int | np.ndarray[int] = None):
        # spline = np.interp(self.center_line[:, 0])
        max_points = 10
        if center_line_index is None:
            car_position = np.array(car_position)
            index, _ = self.get_center_line_index(car_position)
        else:
            index = center_line_index
        index_slice = (np.arange(max_points) + index + 2) % len(self.center_line)
        ref_line = self.center_line[index_slice]
        return ref_line










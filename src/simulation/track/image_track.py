import os

import numpy as np
import pygame
from pygame.colordict import THECOLORS

from src.simulation.track.base import TrackBase
from src.simulation.track.utils.middle_line import get_track_center_line


class ImageTrackBase(TrackBase):
    file_directory = os.path.dirname(__file__)
    directory_path = "image_maps"

    def __init__(self, size: tuple[int, int] | list[int],
                 start_position: tuple[int, int, int] | list[int],
                 map_name: str):
        self.start_position = start_position
        self.size = size
        map_path = f"{self.file_directory}/{self.directory_path}/{map_name}"
        self.game_map: pygame.Surface = pygame.image.load(map_path)
        self.game_map = pygame.transform.scale(self.game_map, size)

        self.center_line = get_track_center_line(map_path, size=size, choice=0)
        super().__init__(self.game_map)


    def draw(self, screen: pygame.Surface, car_position: tuple[int, int]):
        # x = screen.get_width() // 2 - car_position[0]
        # y = screen.get_height() // 2 - car_position[1]
        screen.fill(THECOLORS["white"])
        screen.blit(self.game_map, dest=(0, 0))

    def get_start_position(self):
        return self.start_position

    def get_center_line_index(self, point: np.ndarray, previous_index: int = None):
        if previous_index is not None:
            search_slice = (np.arange(15) - 4 + previous_index) % len(self.center_line)
            center_line = self.center_line[search_slice]
            distance = np.linalg.norm(center_line - point, axis=1)
            return (np.argmin(distance) + search_slice[0]) % len(self.center_line)
        else:
            center_line = self.center_line
            distance = np.linalg.norm(center_line - point, axis=1)
            return np.argmin(distance)

    def get_center_line_in_front(self, car_position: tuple[int, int] = None, center_line_index: int | np.ndarray[int] = None):
        # spline = np.interp(self.center_line[:, 0])
        max_points = 10
        if center_line_index is None:
            car_position = np.array(car_position)
            index = self.get_center_line_index(car_position)
        else:
            index = center_line_index
        index_slice = (np.arange(max_points) + index + 2) % len(self.center_line)
        ref_line = self.center_line[index_slice]
        return ref_line



if __name__ == '__main__':
    pygame.init()
    window_size = (1600, 800)
    screen = pygame.display.set_mode(window_size)
    track = ImageTrackBase(size=window_size, start_position=(710, 690, 0), map_name="map.png")

    track.draw(screen, (0, 0))

    line = track.get_center_line_in_front(car_position=(710, 680))
    for point in line:
        pygame.draw.circle(screen, THECOLORS["red"], point, 1)


    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
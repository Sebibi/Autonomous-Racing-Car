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
        game_map: pygame.Surface = pygame.image.load(map_path)
        game_map = pygame.transform.scale(game_map, size)
        game_map_array = pygame.surfarray.pixels3d(game_map)

        raceline_path = f"{self.file_directory}/optimal_racing_line/{map_name[:-4]}.npy"
        if os.path.exists(raceline_path) and False:
            center_line = np.load(raceline_path)
        else:
            center_line = get_track_center_line(game_map_array, size=size, choice=0)
        super().__init__(game_map, center_line)

    def get_start_position(self):
        return self.start_position


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

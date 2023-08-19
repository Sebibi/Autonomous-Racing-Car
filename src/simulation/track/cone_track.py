import pygame
from pygame.colordict import THECOLORS

from src.simulation.game.object.cone import Cone
from src.simulation.track.base import TrackBase
from src.simulation.track.utils.middle_line import get_track_center_line


class ConeTrackBase(TrackBase):
    inner_cones: list[Cone]
    outer_cones: list[Cone]
    center_line: list[tuple[int, int]]
    start_position = tuple[int, int]
    inner_limit: pygame.Rect
    outer_limit: pygame.Rect

    def __init__(self,
                 size: tuple[int, int] | list[int],
                 inner_track: list[tuple[int, int]],
                 outer_track: list[tuple[int, int]],
                 starting_position: tuple[int, int, int] | list[int]):
        self.inner_cones = [Cone(cone[0], cone[1], THECOLORS['yellow']) for cone in inner_track]
        self.outer_cones = [Cone(cone[0], cone[1], THECOLORS['blue']) for cone in outer_track]

        game_map: pygame.Surface = pygame.Surface(size)
        game_map_array = pygame.surfarray.pixels3d(game_map)
        self.create_game_map(game_map)
        center_line = get_track_center_line(game_map_array, size=size, choice=0)
        self.start_position = starting_position
        super().__init__(game_map, center_line)

    def create_game_map(self, surface: pygame.Surface):
        surface.fill(THECOLORS['white'])
        inner_coords = [cone.get_position() for cone in self.inner_cones]
        outer_coords = [cone.get_position() for cone in self.outer_cones]
        pygame.draw.polygon(surface, THECOLORS['black'], outer_coords, 0)
        pygame.draw.polygon(surface, THECOLORS['white'], inner_coords, 0)

        # for cone in self.inner_cones:
        #     cone.draw(surface)
        #
        # for cone in self.outer_cones:
        #     cone.draw(surface)

    def get_start_position(self):
        return self.start_position




if __name__ == '__main__':
    pygame.init()
    window_size = (1600, 800)
    screen = pygame.display.set_mode(window_size)
    track = ConeTrackBase(size=window_size,
                          inner_track=[(100, 100), (200, 100), (200, 200), (100, 200)],
                          outer_track=[(10, 10), (300, 10), (300, 300), (10, 300)],
                          starting_position=(150, 150, 0))

    track.draw(screen, (0, 0))

    line = track.get_center_line_in_front(car_position=(150, 150))
    for point in line:
        pygame.draw.circle(screen, THECOLORS["red"], point, 1)

    pygame.display.update()
    pygame.time.wait(5000)
    pygame.quit()
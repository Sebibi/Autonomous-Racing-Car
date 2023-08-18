import numpy as np
import pygame
from pygame.colordict import THECOLORS

from src.simulation.game.object.car import PygameCar
from src.simulation.track.base import TrackBase


class Lidar:
    car: PygameCar
    track: TrackBase
    last_obs: list[float]

    max_dist = 500
    step_dist = 5

    def __init__(self, car: PygameCar, track: TrackBase, num_lasers: int):
        self.car = car
        self.track = track
        self.num_lasers = num_lasers
        step = (180 + num_lasers - 1) // num_lasers
        r = np.arange(0, 180, step)
        self.angles = r + (180 - r[-1]) // 2 + 90
        self.rad_angles = np.radians(self.angles)

    def get_lidar_distances(self) -> list[float]:
        if self.car.crashed:
            self.last_obs = [0 for _ in range(self.num_lasers)]
        else:
            self.last_obs = [self.get_lidar_distance(angle) for angle in self.angles]
        return self.last_obs.copy()

    def get_lidar_distance(self, angle) -> float:
        car_position = np.array(self.car.model.get_position(), dtype=np.float64)
        position = car_position.astype(np.float64)
        new_angle = np.radians(self.car.model.angle + angle)
        delta_vector = self.step_dist * np.array([np.cos(new_angle), np.sin(new_angle)])
        for dist in range(0, self.max_dist, self.step_dist):
            position += delta_vector
            if not self.track.in_track_limit(tuple(position.astype(int))):
                return dist / self.max_dist
        return 1

    def draw(self, screen: pygame.Surface):
        car_position = np.array(self.car.model.get_position(), dtype=np.float64)
        for i, (angle, distance) in enumerate(zip(self.angles, self.last_obs)):
            new_angle = np.radians(self.car.model.angle + angle)
            end_laser_position = distance * self.max_dist * np.array([np.cos(new_angle), np.sin(new_angle)]) + car_position
            color = THECOLORS['red'] if i == 0 or i == len(self.angles) - 1 else THECOLORS['yellow']
            pygame.draw.line(screen, color, car_position, end_laser_position, 1)

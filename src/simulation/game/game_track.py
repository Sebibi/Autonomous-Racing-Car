import pygame
import sys

import numpy as np
from pygame.colordict import THECOLORS

from src.simulation.game.object.car import PygameCar
from src.controller.key_board.commands import Commands
from src.simulation.sensor.lidar import Lidar
from src.simulation.track.image_track import ImageTrackBase


class GameTrack:
    track: ImageTrackBase

    def __init__(self, name: str, track: ImageTrackBase, cars: list[PygameCar], screen: pygame.Surface,
                 clock_speed: int = 30):
        self.screen = screen
        self.track = track
        self.cars: np.ndarray(dtype=PygameCar, shape=(-1,)) = np.array(cars)
        self.sensors = [Lidar(car, track, 9) for car in self.cars]
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.round = 0
        self.best_car: PygameCar = self.cars[0]
        self.clock_speed = clock_speed
        pygame.display.set_caption(name)
        self.center_line = []

    def update(self, commands: list[str] | list[list[float]]) -> list[list[float]]:
        self.track.draw(car_position=self.best_car.model.get_position(), screen=self.screen)
        center_line = self.track.get_center_line_in_front(self.best_car.model.get_position())
        self.center_line = (center_line / np.array([self.track.size[0], self.track.size[1]])).flatten().tolist()
        for point in center_line:
            pygame.draw.circle(self.screen, THECOLORS["red"], point, 1)
        # pygame.draw.circle(self.track.screen, THECOLORS['red'], self.best_car.rect.center, 100)
        for command, car in zip(commands, self.cars):
            if not car.crashed:
                car.draw(self.screen, self.best_car.model.get_position())
                if car.score > self.best_car.score:
                    self.best_car = car
                car.update(command)
                if len(self.cars) > 1:
                    self.best_car.color = THECOLORS['yellow']

        for car in self.cars:

            if not car.crashed:
                in_track_limit = self.track.in_track_limit(car.model.get_state()[:2])
                if not in_track_limit:
                    car.crashed = True

        sensor_values = [sensor.get_lidar_distances() for sensor in self.sensors]

        self.game_over = all([car.crashed for car in self.cars]) or self.round > 1800
        self.round += 1
        self.clock.tick(self.clock_speed)
        return sensor_values

    def get_observation(self, sensor_values: list[list[float]]):
        lines = []
        for car in self.cars:
            track_size = np.array([self.track.size[0], self.track.size[1]])
            center_line = self.track.get_center_line_in_front(car.model.get_position()) / track_size
            lines.append(center_line.flatten().tolist())

        car_pos = np.array([car.model.get_position() for car in self.cars])
        car_pos = car_pos / track_size
        return [sensor_values[i]
                + list(car_pos[i])
                + [self.cars[i].model.get_velocity(), self.cars[i].model.get_angle()]
                + lines[i]
                for i in range(len(self.cars))]

    def run(self, command_func: callable = Commands.get_from_key_board):
        running = True
        sensor_values = self.update(["None"] * len(self.cars))
        while running and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            commands = [command_func(sensor) for sensor in sensor_values]
            sensor_values = self.update(commands)
        pygame.quit()




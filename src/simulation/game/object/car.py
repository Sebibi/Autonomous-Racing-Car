import os.path

import pygame
from pygame import Color
from pygame.colordict import THECOLORS

from src.simulation.game.object.base import PygameObject
from src.simulation.system.car_model import CarModel
from src.simulation.track.base import TrackBase


class PygameCar(PygameObject):
    model: CarModel
    rect: pygame.Rect
    score: int
    crashed: bool

    radius = 7
    color = THECOLORS['red']

    def __init__(self, model: CarModel):
        self.model = model
        x, y = self.model.get_state()[:2]
        radius = PygameCar.radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 4, radius * 2)
        self.surface = pygame.image.load(os.path.dirname(__file__) + "/car.png")
        self.surface = pygame.transform.scale(self.surface, (radius * 4, radius * 2))
        self.surface = pygame.transform.rotate(self.surface, 180)
        self.color = PygameCar.color
        self.crashed = False
        self.score = 0

    def continuous_update(self, accel: float, steering: float):
        if self.crashed:
            return
        assert -1 <= accel <= 1, "Speed must be between 0 and 1 but is {}".format(accel)
        assert -1 <= steering <= 1, "Angular accel must be between -1 and 1 but is {}".format(steering)
        self.model.update(accel, steering)
        self.rect.center = self.model.get_position()
        v = self.model.get_velocity()
        self.color = Color(int(255 * (1 - v)), int(255 * v), 0)
        self.score += (abs(v) * 100) + 1
        # - abs(steering * steering) * 20
        # - abs(accel) * 5
        # + 1)

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def blitRotateCenter(self, surf, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, -angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
        surf.blit(rotated_image, new_rect)
        # pygame.draw.rect(surf, THECOLORS['blue'], new_rect, 1)

    def draw(self, surface, best_car_position: tuple[float, float] = None):
        delta_x = self.model.x - best_car_position[0]
        delta_y = self.model.y - best_car_position[1]
        # self.surface = pygame.Surface((self.radius * 4, self.radius * 2))
        # self.surface.fill(self.color)
        pygame.draw.circle(self.surface, self.color, (self.surface.get_width() // 1.5, self.surface.get_height() // 2), 7)
        # self.rect.center = (surface.get_width() // 2 + delta_x, surface.get_height() // 2 + delta_y)
        self.blitRotateCenter(surface, self.surface, self.rect.topleft, self.model.angle)
        # surface.blit(self.surface, self.rect.center)

    def set_position(self, position: tuple[int, int, int]):
        self.model.x = position[0]
        self.model.y = position[1]
        self.model.angle = position[2]
        self.rect.center = self.model.get_position()

    @staticmethod
    def get_normal_car(track: TrackBase):
        start_pos = track.get_start_position()
        model = CarModel(*start_pos, v=1, v_max=15, a_max=0.5, steering_max=120, L=90)
        return PygameCar(model=model)

    def update(self, command: str | list[float]):
        if isinstance(command, list):
            assert len(command) == 2, f"Command must be a list of 2 elements but {command}"
            self.continuous_update(accel=command[0], steering=command[1])
        else:
            accel = 0.2
            angular_speed = 1
            if self.crashed:
                return
            if command == "up":
                self.continuous_update(accel, 0)
            if command == "down":
                self.continuous_update(-accel, 0)
            if command == "left":
                self.continuous_update(0, angular_speed)
            if command == "right":
                self.continuous_update(0, -angular_speed)
            if command == "None":
                self.continuous_update(0, 0)

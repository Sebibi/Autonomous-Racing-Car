import sys
import time

import pygame

from src.controller.key_board.commands import Commands
from src.controller.machine_learning.neat.deploy import NeatController
from src.simulation.game.game_track import GameTrack
from src.simulation.game.object.car import PygameCar
from src.simulation.track.image_track import ImageTrackBase


def main_neat():
    pygame.init()
    window_size = (1600, 800)
    screen = pygame.display.set_mode(window_size)

    neat_controller = NeatController("winner_9laser_new_cost.pkl")
    keyboard_controller = Commands()

    maps: list[str] = ["map.png", "map2.png", "map3.png", "map6.png"]
    # position = [830, 920]  # Starting Position
    for map_name in maps[:]:
        track = ImageTrackBase(
            size=window_size,
            start_position=(710, 700, 180),
            map_name=map_name
        )

        car1 = PygameCar.get_normal_car(track)
        car2 = PygameCar.get_normal_car(track)
        car2.model.x -= 50
        car2.model.y += 0

        game = GameTrack(
            name="NEAT controller",
            track=track,
            cars=[car1],
            screen=screen,
            clock_speed=30,
        )

        obs = game.update(["None"] * len(game.cars))
        obs = [obs[i] + [game.cars[i].model.get_position()] for i in range(len(game.cars))]

        track.draw(screen=screen, car_position=car1.model.get_state()[:2])
        for car in game.cars:
            car.draw(screen, car1.model.get_state()[:2])
        pygame.display.update()

        time.sleep(1)
        while not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            controls = [neat_controller.get_command(obs[i]) for i in range(len(game.cars))]
            # controls = [Commands.get_from_key_board()] * len(game.cars)
            obs = game.update(controls)
            obs = game.get_observation(obs)
            pygame.display.update()


if __name__ == '__main__':
    main_neat()
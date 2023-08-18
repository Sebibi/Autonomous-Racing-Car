import os
import pickle
import sys
import time

import neat
import pygame

from src.simulation.game.game_track import GameTrack
from src.simulation.game.object.car import PygameCar
from src.simulation.track.image_track import ImageTrackBase


def eval_genomes(genomes, config):
    pygame.init()
    window_size = (1600, 800)
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    track = ImageTrackBase(map_name="map8.png", start_position=(710, 680, 180), size=window_size)
    # track = RectangleTrack(1000, 700, 100, center)
    cars = [PygameCar.get_normal_car(track) for _ in genomes]

    game = GameTrack(name="NEAT training", track=track, cars=cars, screen=screen, clock_speed=1200)
    sensor_read = game.update(["None"] * len(genomes))
    nets = [neat.nn.FeedForwardNetwork.create(genome, config) for _, genome in genomes]
    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        obs = game.get_observation(sensor_read)
        commands = [net.activate(obs[i]) for i, net in enumerate(nets)]
        sensor_read = game.update(commands)
        pygame.display.update()

    for i, (_, genome) in enumerate(genomes):
        genome.fitness = game.cars[i].score

    time.sleep(1)


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-44')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(15))

    winner = p.run(eval_genomes, 1000)
    print("Best genome:\n{!s}".format(winner))
    with open("src/controller/machine_learning/neat/data/models/winner_9laser_new_cost.pkl", "wb") as f:
        pickle.dump(winner, f)
    return winner


def main_neat():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'data/config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)

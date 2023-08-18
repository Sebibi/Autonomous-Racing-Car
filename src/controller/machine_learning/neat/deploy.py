import pickle
import os
import neat

from src.controller.key_board.commands import Commands


class NeatController:
    neat_directory = os.path.dirname(__file__)
    model_directory: str = "data/models"
    config_file_path: str = "data/config.txt"

    def __init__(self, model_name):
        model_file_path = f"{self.neat_directory}/{self.model_directory}/{model_name}"
        with open(model_file_path, "rb") as f:
            model = pickle.load(f)

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             f"{self.neat_directory}/{self.config_file_path}")
        self.net = neat.nn.FeedForwardNetwork.create(model, config)

    def get_command(self, sensor_read: list[float]) -> list[float]:
        return self.net.activate(sensor_read)

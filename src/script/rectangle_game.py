from src.controller.machine_learning.neat import NeatController
from src.simulation.game.game_track import GameTrack
from src.simulation.system import PygameCar
from src.simulation.track.cone_maps.rectangle import RectangleTrack

if __name__ == '__main__':
    window_size = (1600, 800)
    center = (window_size[0] // 2, window_size[1] // 2)
    track = RectangleTrack(1000, 700, 100, center)
    car = PygameCar.get_normal_car(track)

    neat_controller = NeatController("../controller/machine_learning/neat/winner2.pkl",
                                     "../controller/machine_learning/neat/config.txt")
    game = GameTrack(track, [car], window_size=window_size)
    game.run(neat_controller.get_command)



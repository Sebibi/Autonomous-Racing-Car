import os
import random
import sys

import gymnasium as gym
import numpy as np
import pygame.sysfont
import stable_baselines3
from gymnasium import spaces
from stable_baselines3 import PPO

sys.path.append(f"{os.path.dirname(__file__)}/../../../")

from src.simulation.game.object.car import PygameCar
from src.simulation.sensor.lidar import Lidar
from src.simulation.track.image_track import ImageTrackBase
from stable_baselines3.common.callbacks import BaseCallback


class StopTrainingCallback(BaseCallback):
    def __init__(self, stopping_condition, verbose=0):
        super(StopTrainingCallback, self).__init__(verbose)
        self.stopping_condition = stopping_condition

    def _on_step(self) -> bool:
        if self.stopping_condition:
            # Stop training by returning False
            return False
        else:
            # Continue training
            return True


class FormulaStudentv1(gym.Env):
    observation_space: spaces.Space
    action_space: spaces.Space

    def __init__(self, render_mode: str = "human", clock_speed: int = 120):
        self.start_index = None
        self.observation_space = spaces.Box(low=0, high=1, shape=(11,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        window_size = (1600, 800)

        # Pygame elements for rendering
        pygame.init()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.screen = pygame.display.set_mode(window_size) if render_mode == 'human' else None

        self.track: ImageTrackBase = None
        self.car: PygameCar = None
        self.sensor: Lidar = None
        self.step_count = 0
        self.reset_count = -1
        self.previous_closest_point = None

        self.reset()

        if self.screen:
            self.track.draw(self.screen, self.car.model.get_position())
            for point in self.track.center_line:
                pygame.draw.circle(self.screen, (0, 255, 0), point, 2)
            pygame.display.update()
            pygame.time.wait(2000)

    def create_obs(self) -> np.ndarray[float]:
        sensor = self.sensor.get_lidar_distances()
        # car_position = np.array(self.car.model.get_position()) / np.array(self.track.size)
        # car_position = car_position.flatten().tolist()
        # centerline = self.track.get_center_line_in_front(center_line_index=self.previous_closest_point) / np.array(
        #    self.track.size)
        # centerline = centerline.flatten().tolist()
        velocity = self.car.model.get_velocity()
        angle = self.car.model.get_angle()
        obs = sensor + [velocity, angle]
        assert len(obs) == 11, f"Observation length is {len(obs)}, should be 11"
        return np.array(obs)

    def reset(self, **kwargs):
        maps = ["map11.png"]  # ["map.png", "map2.png", "map8.png", "map11.png"]
        map_name = maps[(self.reset_count // 5) % len(maps)]
        if kwargs.get("track_index"):
            map_name = maps[kwargs["track_index"] % len(maps)]
        self.reset_count += 1
        print(map_name)
        self.track = ImageTrackBase(size=(1600, 800), map_name=map_name, start_position=(710, 710, 180))
        self.car = PygameCar.get_normal_car(self.track)
        self.sensor = Lidar(self.car, self.track, 9)
        self.step_count = 0

        start_index = random.randint(0, len(self.track.center_line) - 1)
        self.start_index = start_index
        if start_index % 2 == 1:
            self.track.center_line = self.track.center_line[::-1]
        position = self.track.center_line[start_index]
        delta_pos = self.track.center_line[(start_index + 1) % len(self.track.center_line)] - position
        angle = np.arctan2(-delta_pos[1], -delta_pos[0]) * 180 / np.pi
        self.car.set_position((position[0], position[1], angle))
        self.previous_closest_point = start_index

        obs = self.create_obs()
        return np.array(obs), {}

    def step(self, action):
        self.step_count += 1
        action = action.tolist()
        self.car.update(action)

        # Check the track limits
        in_track = self.track.in_track_limit(self.car.model.get_position())

        # Compute progress on track
        new_closest_point, distance = self.track.get_center_line_index(
            point=np.array(self.car.model.get_position()),
            previous_index=self.previous_closest_point
        )
        delta_index = (new_closest_point - self.previous_closest_point) % len(self.track.center_line)
        if delta_index > 64:
            delta_index = 0
            print(f"Delta index is to big {delta_index} {new_closest_point} {self.previous_closest_point}")
        self.previous_closest_point = new_closest_point

        obs = self.create_obs()
        # laser = obs[:9]
        # delta_laser = abs(laser[0] - laser[-1])
        # center_laser_sum = sum(laser[3:6])
        # side_laser_sum = laser[0] + laser[-1]
        # delta_center_side = center_laser_sum - 1.2 * side_laser_sum

        # Compute the score
        track_width = (obs[0] + obs[8]) * Lidar.max_dist / 2
        center_line_distance = distance / track_width
        next_closest_point = (self.previous_closest_point + 1) % len(self.track.center_line)
        points = self.track.center_line[[self.previous_closest_point, next_closest_point]]
        vector = points[1] - points[0]
        angle = np.arctan2(-vector[1], -vector[0]) / (2 * np.pi)
        angle = angle + 1 if angle < 0 else angle
        delta_heading = abs(angle - self.car.model.get_angle())
        delta_heading = min(delta_heading, 1 - delta_heading) / 0.5
        # print(f"Delta heading {delta_heading}")
        steering_angle = self.car.model.get_steering_angle()
        delta_steering = abs(steering_angle - 0.5)

        center_line_distance = min(1, center_line_distance)
        delta_heading = min(1, delta_heading)
        score = 20 * delta_index - 2 * delta_steering ** 2 - 5 * center_line_distance - 5 * delta_heading - 5
        done = not in_track
        truncated = self.step_count > 600  # self.previous_closest_point == (self.start_index - 1) % len(self.track.center_line)
        if done:
            score -= 500
        self.clock.tick(self.clock_speed)
        return obs, score, done, truncated, {}

    def render(self, mode='human'):
        self.track.draw(screen=self.screen, car_position=self.car.model.get_position())
        self.car.draw(self.screen, self.car.model.get_position())
        self.sensor.draw(self.screen)
        center_line = self.track.get_center_line_in_front(self.car.model.get_position())
        for point in center_line:
            pygame.draw.circle(self.screen, (0, 255, 0), point, 1)
        pygame.display.update()


gym.register(
    id='FormulaStudentv1-v1',
    entry_point='formula_student_module:FormulaStudentv1',
)


def test_env(model: stable_baselines3.PPO = None):
    env = FormulaStudentv1(render_mode="human", clock_speed=30)
    track_index = 0  # int(input("Track index: "))
    obs, info = env.reset(track_index=track_index)
    done = False
    truncated = False
    sum_reward = 0
    while not done and not truncated:
        if model:
            action, _ = model.predict(obs, deterministic=True)
        else:
            action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        sum_reward += reward
        print("Reward", reward)
    env.close()
    pygame.quit()

    print("Sum reward", sum_reward)


if __name__ == '__main__':

    gamma = 0.99
    # test_env()

    file_name = "formula_student_ppo_99_race_line_cost"

    retest = True
    if os.path.exists(f"{file_name}.zip"):
        model = PPO.load(f"{file_name}.zip", gamma=gamma)
    else:
        model = None
    while retest:
        test_env(model=model)
        retest = input("Retest? (y/n)") == "y"

    train = input("Train? (y/n)") == "y"
    if train:
        env = FormulaStudentv1(render_mode="ai", clock_speed=200)
        if os.path.exists(f"{file_name}.zip"):
            print("Loading model")
            model = PPO.load(f"{file_name}.zip", env=env, gamma=gamma)
        else:
            print("Creating model")
            model = PPO("MlpPolicy", env, verbose=1, gamma=gamma)
        print(model.observation_space, model.action_space)
        model.learn(total_timesteps=200_000, progress_bar=False)
        model.save(file_name)
        env.close()

    print("Testing model")
    model = PPO.load(f"{file_name}.zip", gamma=gamma)
    test_env(model=model)

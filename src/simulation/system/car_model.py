import math

import numpy as np


class CarModel:

    def __init__(self, x: int, y: int, angle: float, v: int, v_max: int = 40, a_max: float = 2, L=150,
                 steering_max: int = 60):
        # Position
        self.x = x
        self.y = y

        # Velocity
        self.v = v
        self.v_max = v_max
        self.a_max = a_max

        # Steering
        self.angle = angle
        self.steering = steering_max // 2
        self.steering_max = steering_max
        self.L = L

    def update(self, accel: float, steering: float):
        self.v += accel * self.a_max
        self.v = max(2, self.v)
        self.v = min(self.v, self.v_max)

        self.steering = (steering + 1) * 0.5 * self.steering_max

        grip = self.grip_coefficient(self.v, self.steering)
        delta_angle = self.v / self.L * math.tan(np.radians(self.steering - (self.steering_max // 2))) * grip
        self.angle += delta_angle * 180 / math.pi
        self.angle %= 360

        self.x += -self.v * math.cos(np.radians(self.angle))
        self.y += -self.v * math.sin(np.radians(self.angle))

    def grip_coefficient(self, velocity, steering_angle):
        # Define the grip coefficient as a function of velocity and steering angle
        max_grip = 1.0  # Maximum grip coefficient
        min_grip = 0.2  # Minimum grip coefficient
        grip = max_grip - 0.8 * (velocity / self.v_max)  # Grip decreases with velocity
        return max(min_grip, grip)

    def get_state(self) -> tuple[int, int, float, float]:
        return int(self.x), int(self.y), self.angle, -self.v

    def get_position(self) -> tuple[int, int]:
        return int(self.x), int(self.y)

    def get_steering_angle(self) -> float:
        return self.steering / self.steering_max

    def get_angle(self) -> float:
        return self.angle / 360.0

    def get_velocity(self) -> float:
        return self.v / self.v_max

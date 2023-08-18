import math

import numpy as np

from src.simulation.track.cone_track import ConeTrackBase


def create_scattered_circle(radius, center, spacing_angle: int = None, num_cones: int = None):
    positions = []
    if spacing_angle is None:
        spacing_angle = 360 // num_cones
    for i in range(0, 360, spacing_angle):
        x = center[0] + int(radius * math.cos(math.radians(i)))
        y = center[1] + int(radius * math.sin(math.radians(i)))
        positions.append((x, y))
    return np.around(positions).astype(int).tolist()


class CircleTrack(ConeTrackBase):

    def __init__(self, inner_radius: int, outer_radius: int, track_center: tuple[int, int] | list[int],
                 cone_spacing: int = 30):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.track_center = track_center
        self.start_position = (track_center[0] + (inner_radius + outer_radius) // 2, track_center[1])

        inner_track = create_scattered_circle(inner_radius, track_center, cone_spacing)
        outer_track = create_scattered_circle(outer_radius, track_center, cone_spacing)
        middle_track = create_scattered_circle((inner_radius + outer_radius) // 2, track_center, cone_spacing)
        super().__init__(inner_track, outer_track, middle_track)

    def get_start_position(self):
        return list(self.start_position) + [90]


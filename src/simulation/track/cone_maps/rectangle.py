from src.simulation.track.cone_track import ConeTrackBase


def add_offset_to_list(list_to_add: list[tuple[int, int]], offset: tuple[int, int]):
    return [(x + offset[0], y + offset[1]) for x, y in list_to_add]


class RectangleTrack(ConeTrackBase):

    def __init__(self, length: int, height: int, track_width: int, track_center: tuple[int, int] | list[int]):
        self.length = length
        self.height = height
        self.track_width = track_width
        self.start_position = (length - track_width // 2, height // 2)
        self.outer_track = [(0, 0), (length, 0), (length, height), (0, height)]
        self.inner_track = [(track_width, track_width), (length - track_width, track_width),
                            (length - track_width, height - track_width), (track_width, height - track_width)]
        self.middle_track = [(length // 2, track_width), (length - track_width, height // 2),
                             (length // 2, height - track_width), (track_width, height // 2)]

        offset = (track_center[0] - length // 2, track_center[1] - height // 2)
        self.start_position = add_offset_to_list([self.start_position], offset)[0]
        self.inner_track = add_offset_to_list(self.inner_track, offset)
        self.outer_track = add_offset_to_list(self.outer_track, offset)
        self.middle_track = add_offset_to_list(self.middle_track, offset)

        super().__init__(self.inner_track, self.outer_track, self.middle_track)

    def get_start_position(self):
        return list(self.start_position) + [90]


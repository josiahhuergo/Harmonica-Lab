from piano_roll.state import piano_roll_state as state


def pitch_to_y(pitch: int) -> int:  # piano roll utilities
    """Takes a pitch integer and returns the y position of the
    top of the corresponding key lane in the piano roll."""

    return int((state.max_pitch - pitch) * state.key_height)


def time_to_x(beat: float) -> int:  # piano roll utilities
    """Takes a point in time and translates it into a pixel position."""

    return int(state.beat_width * beat)


def y_to_pitch(y: int) -> int:  # piano roll utilities
    """Takes a y position in pixels and returns the pitch of the key
    lane at that position."""

    return int(state.max_pitch - (y / state.key_height))


def x_to_time(x: int) -> float:  # piano roll utilities
    """Takes an x position in pixels and returns the point in time
    at that position."""

    return x // state.beat_width


zoom_x: float = 1.0  # PianoRollViewState

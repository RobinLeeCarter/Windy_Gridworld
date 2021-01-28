import numpy as np

import common
from environment import grid

rng: np.random.Generator = np.random.default_rng()


def racetrack_test1() -> bool:
    racetrack_ = grid.GridWorld(grid.TRACK_1, rng)
    assert racetrack_.get_square(0, 0) == common.Square.START
    assert racetrack_.get_square(5, 0) == common.Square.OBSTACLE
    assert racetrack_.get_square(5, 6) == common.Square.END
    assert racetrack_.get_square(0, 6) == common.Square.NORMAL

    assert racetrack_.get_square(-1, -1) == common.Square.OBSTACLE
    assert racetrack_.get_square(6, 7) == common.Square.OBSTACLE
    assert racetrack_.get_square(6, 6) == common.Square.END
    assert racetrack_.get_square(10, 6) == common.Square.END
    assert racetrack_.get_square(-1, 6) == common.Square.OBSTACLE

    for _ in range(10):
        x, y = racetrack_.get_a_start_position()
        print(f"start position = ({x}, {y})")

    return True


if __name__ == '__main__':
    if racetrack_test1():
        print("Passed")

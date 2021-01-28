import numpy as np

import view
from environment import grid

rng: np.random.Generator = np.random.default_rng()


def view_test() -> bool:
    racetrack_ = grid.GridWorld(grid.TRACK_3, rng)
    my_view = view.View(racetrack_)
    my_view.open_window()
    my_view.display_and_wait()

    return True


if __name__ == '__main__':
    if view_test():
        print("Passed")

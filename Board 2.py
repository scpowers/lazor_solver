
class Board:

    def __init__(self, initial_board, laser_pos, laser_dir):
        self.board = initial_board  # initial config of board (with everything on it)
        self.laser_pos = laser_pos  # [x, y] position of laser source on grid where cells are 3x3 across
        self.laser_dir = laser_dir  # [dx, dy] direction of laser source on grid where cells are 3x3 across

    # TODO: modify_board - adjust board configuration

    # TODO: get_laser_path - compute and return sequence of points the laser visits
    def laser_path(self):
        # convert board into grid where cells are 3x3 across
        pass

    # TODO: render_board - draw board config + laser as grid image and save it

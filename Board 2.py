import numpy as np

class Board:

    def __init__(self, initial_board, laser_pos, laser_dir):
        self.board = initial_board  # initial config of board (with everything on it)
        self.laser_pos = laser_pos  # [x, y] position of laser source on grid where cells are 3x3 across
        self.laser_dir = laser_dir  # [dx, dy] direction of laser source on grid where cells are 3x3 across

    # TODO: modify_board - adjust board configuration

    # TODO: get_laser_path - compute and return sequence of points the laser visits
    def laser_path(self):
        # convert board into grid where cells are 3x3 across
        new_board = np.zeros((3*len(self.board), 3*len(self.board)))
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    continue

                new_board[3*i:3*(i+1), 3*j:3*(j+1)] = cell

        print(f'new board:\n {new_board}')

    # TODO: render_board - draw board config + laser as grid image and save it
    # Maranda
    def render_board():

        return []

if __name__ == '__main__':
    formatted_board = [[0, 0, 1, 0],
                       [2, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 1, 0, 0]]
    test_board = Board(formatted_board, [1, 1], [1, 1])
    test_board.laser_path()

import numpy as np

class Board:

    def __init__(self, initial_board, laser_pos, laser_dir):
        self.board = initial_board  # initial config of board (with everything on it)
        self.laser_pos = laser_pos  # [x, y] position(s) of laser source(s) on grid where cells are 3x3 across
        self.laser_dir = laser_dir  # [dx, dy] direction(s) of laser source(s) on grid where cells are 3x3 across
        self.laser_visited_pts = []  # initialize empty list, need it later for rendering

    # TODO: modify_board - adjust board configuration

    # TODO: get_laser_path - compute and return sequence of points the laser visits
    def get_laser_path(self):
        # convert board into grid where cells are 3x3 across
        new_board = np.zeros((2*len(self.board) + 1, 2*len(self.board) + 1))
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    continue

                new_board[2*i + 1, 2*j + 1] = cell

        # NOTE: transpose because coord system is opposite order from (row, col) accessing in the array
        new_board = np.transpose(new_board)
        print(f'new board:\n {new_board}')

        # check if a given position is within the gridded board
        def pos_check(coord_board, coords):
            return 0 <= coords[0] < coord_board.shape[0] and 0 <= coords[1] < coord_board.shape[1]

        # initialize list of visited points across all laser sources
        total_visited_pts = []
        for i, pos in enumerate(self.laser_pos):
            # initialize stack, build from starting point, backtrack if you exit grid or hit opaque block,
            # only able to continue after backtracking if another route exists because of a refraction block
            laser_path = [pos]
            direction = self.laser_dir[i]  # initial direction pulled from .bff file
            max_path_length = 50
            iter = 0
            # keep going until you've emptied the stack or you hit the upper bound on path length
            # (prevents infinite loops)
            while len(laser_path) > 0 and iter < max_path_length:
                # add most recent position to total visited pts if it's unique and within the board
                latest_pos = laser_path[-1]
                if pos_check(new_board, latest_pos) and latest_pos not in total_visited_pts:
                    total_visited_pts.append(latest_pos)

                # compute next position/direction
                # case 1: latest position is within a vertical slice between cells
                if latest_pos[0] % 2 == 0:
                    if direction[0] > 0:
                        next_relevant_center_coords = [latest_pos[0] + 1, latest_pos[1]]
                    else:
                        next_relevant_center_coords = [latest_pos[0] - 1, latest_pos[1]]
                # case 2: latest position is within a horizontal slice between cells
                else:
                    if direction[1] > 0:
                        next_relevant_center_coords = [latest_pos[0], latest_pos[1] + 1]
                    else:
                        next_relevant_center_coords = [latest_pos[0], latest_pos[1] - 1]

                # check cell behavior at the next relevant center
                # but first: check that it's actually a cell
                if not pos_check(new_board, next_relevant_center_coords):
                    print('next relevant center is off the grid...end of this laser path')
                    break  # backtracking not implemented yet

                # case 1: the next relevant cell is empty
                if new_board[next_relevant_center_coords[0], next_relevant_center_coords[1]] == 0:
                    next_pos = [latest_pos[0] + direction[0], latest_pos[1] + direction[1]]  # move normally by one step
                    next_direction = direction  # direction is unchanged
                # case 2: the next relevant cell is a reflective cell, so change direction
                elif new_board[next_relevant_center_coords[0], next_relevant_center_coords[1]] == 1:
                    print('encountered a reflective cell')
                    next_pos = latest_pos  # position is unchanged
                    # if you're in a vertical slice between cells, just changing dx
                    if latest_pos[0] % 2 == 0:
                        next_direction = [-1 * direction[0], direction[1]]
                    else:
                        next_direction = [direction[0], -1 * direction[1]]
                else:
                    print('cell type not supported yet')
                    break

                # update
                laser_path.append(next_pos)
                direction = next_direction
                iter += 1

        # store visited points as attribute
        self.laser_visited_pts = total_visited_pts

    # TODO: render_board - draw board config + laser as grid image and save it
    # Maranda
    def render_board():

        return []

if __name__ == '__main__':
    formatted_board = [[0, 0, 0, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 2],
                       [0, 0, 1, 0]]
    test_board = Board(formatted_board, [[2, 7]], [[1, -1]])
    test_board.get_laser_path()
    print(f'{test_board.laser_visited_pts}')

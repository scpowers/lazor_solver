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
        # convert board into grid using same convention as .bff file
        new_board = np.zeros((2*len(self.board) + 1, 2*len(self.board) + 1))
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    continue

                new_board[2*i + 1, 2*j + 1] = cell

        # NOTE: transpose because coord system is opposite order from (row, col) accessing in the array
        new_board = np.transpose(new_board)
        print(f'new board:\n {new_board}')

        # initialize dict where each key is a laser initial position/direction pair (unique) and
        # each value is a list of visited coordinates in order [[x1, y1], [x2, y2]]
        total_visited_pts = {}
        for i, pos in enumerate(self.laser_pos):
            total_visited_pts[(tuple(pos), tuple(self.laser_dir[i]))] = []

        # now compute the traveled path for each laser source
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
                # add most recent position to total visited pts for this laser source if it's within the board
                latest_pos = laser_path[-1]
                if pos_check(new_board, latest_pos):
                    total_visited_pts[(tuple(pos), tuple(self.laser_dir[i]))].append(latest_pos)

                # get the coordinates of the next relevant cell center (relevant for path behavior at next step)
                next_relevant_center_coords = get_next_relevant_cell_center(latest_pos, direction)

                # check cell behavior at the next relevant center
                should_path_end = should_laser_path_end(new_board, next_relevant_center_coords)
                if should_path_end:
                    print('apparently the path either went off the grid or hit an opaque block')
                    break

                # get the position and direction of the next step in the laser path
                next_pos, next_direction = get_next_laser_pos_dir(new_board, next_relevant_center_coords, latest_pos,
                                                                  direction)

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


# check if a given position is within the gridded board
def pos_check(coord_board, coords):
    return 0 <= coords[0] < coord_board.shape[0] and 0 <= coords[1] < coord_board.shape[1]


# get next relevant cell center
def get_next_relevant_cell_center(latest_pos, direction):
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
    return next_relevant_center_coords


# get next position and direction of the laser path
def get_next_laser_pos_dir(new_board, next_relevant_center_coords, latest_pos, direction):
    next_relevant_cell_val = new_board[next_relevant_center_coords[0], next_relevant_center_coords[1]]
    # case 1: the next relevant cell is empty or a hole
    if next_relevant_cell_val == 0 or next_relevant_cell_val == 5:
        next_pos = [latest_pos[0] + direction[0], latest_pos[1] + direction[1]]  # move normally by one step
        next_direction = direction  # direction is unchanged
    # case 2: the next relevant cell is a reflective cell, so change direction
    elif next_relevant_cell_val == 1:
        print('encountered a reflective cell')
        next_pos = latest_pos  # position is unchanged
        # if you're in a vertical slice between cells, just changing dx
        if latest_pos[0] % 2 == 0:
            next_direction = [-1 * direction[0], direction[1]]
        else:
            next_direction = [direction[0], -1 * direction[1]]
    else:
        raise ValueError(f'cell type {next_relevant_cell_val} not supported yet')

    return next_pos, next_direction


# helper method to determine whether the next relevant cell implies that the laser path should end here
def should_laser_path_end(new_board, next_relevant_center_coords):
    # just care whether the next cell is off the board OR it's an opaque cell
    if not pos_check(new_board, next_relevant_center_coords) or new_board[next_relevant_center_coords[0],
                                                                          next_relevant_center_coords[1]] == 5:
        return True
    else:
        return False

if __name__ == '__main__':
    formatted_board = [[0, 0, 0, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 2],
                       [0, 0, 1, 0]]
    test_board = Board(formatted_board, [[2, 7]], [[1, -1]])
    test_board.get_laser_path()
    print(f'{test_board.laser_visited_pts}')

from Board import Board
import numpy as np
from copy import deepcopy
import time


class LazorSolver:

    def __init__(self, file_ptr):
        initial_board = self.parse_bff(file_ptr)
        self.board = Board(initial_board)
        self.solve()

    def parse_bff(self, file_ptr):
        # TODO: parse .bff and return list or dict describing initial board config
        return []

    # TODO: solve - adjust board configuration until the puzzle is solved
    def solve(self):
        pass


def generate_possible_configs(starting_board):
    free_site_idxs = [i for i, block in enumerate(starting_board) if block != 3]
    print(f'indices of free sites for block placement: {free_site_idxs}')
    num_free_sites = len(free_site_idxs)
    print(f'number of free sites for block placement: {num_free_sites}')
    blocks_to_place = [block for block in starting_board if block == 1 or block == 2 or block == 4]
    print(f'blocks to place: {blocks_to_place}')
    unique_blocks_to_place = set(blocks_to_place)
    print(f'unique blocks to place: {unique_blocks_to_place}')

    empty_board = np.array([0 if i != 3 else i for i in starting_board])

    possible_configs = recurse_generate_boards(empty_board, blocks_to_place, free_site_idxs)
    # convert from 1D numpy arrays to 2D nested Python lists
    possible_configs = [*set([tuple(arr) for arr in possible_configs])]
    possible_configs = [np.array(arr) for arr in possible_configs]
    size = int(np.sqrt(len(starting_board)))
    possible_configs = [arr.reshape(size, size) for arr in possible_configs]
    possible_configs = [[list(arr) for arr in sublist] for sublist in possible_configs]
    possible_configs = [list(arr) for arr in possible_configs]
    return possible_configs


def recurse_generate_boards(input_board, blocks_to_place, free_site_idxs):
    # base case: no more blocks to place, return input_board
    if len(blocks_to_place) == 0:
        return [input_board]

    list_of_returned_configs = []  # should only hold complete, valid board configs
    visited_blocks = []

    for i, block in enumerate(blocks_to_place):  # for each unique block still left to place at this level
        if block in visited_blocks:
            continue

        visited_blocks.append(block)

        # for each free site where you can place this block in the input board
        for j, site in enumerate(free_site_idxs):
            updated_board = deepcopy(input_board)
            updated_board[site] = block  # place the block
            # recursive call with updated board and lists
            updated_blocks_to_place = deepcopy(blocks_to_place)
            updated_blocks_to_place.pop(i)
            updated_free_site_idxs = deepcopy(free_site_idxs)
            updated_free_site_idxs.pop(j)
            received_boards = recurse_generate_boards(updated_board, updated_blocks_to_place, updated_free_site_idxs)

            list_of_returned_configs += received_boards  # add received boards to list of boards to return

    return list_of_returned_configs


if __name__ == '__main__':
    # for now, say 0 = free, 1 = reflect block, 2 = refract block
    starting_board = np.array([[0, 0, 1, 0],
                               [2, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 0, 0]])
    starting_board = starting_board.flatten()
    print(f'{starting_board}')

    points_to_hit = [[3, 0], [4, 3], [2, 5], [4, 7]]

    start = time.perf_counter()
    possible_configs = generate_possible_configs(starting_board)
    print(len(possible_configs))
    print(f'{possible_configs[0]}')

    for config in possible_configs:
        tmp = Board(config, [[2, 7]], [[1, -1]])
        tmp.get_laser_path()

        total_visited_pts = []
        for val in list(tmp.laser_visited_pts.values()):
            total_visited_pts += val

        if not np.any([pt not in total_visited_pts for pt in points_to_hit]):
            print('supposedly found solution')
            print(f'{config}')
            break
    end = time.perf_counter()
    print(f'elapsed time for first board solving: {end - start}')

    start = time.perf_counter()
    possible_configs = generate_possible_configs(starting_board)
    print(len(possible_configs))
    print(f'{possible_configs[0]}')

    for config in possible_configs:
        tmp = Board(config, [[2, 7]], [[1, -1]])
        tmp.get_laser_path()

        total_visited_pts = []
        for val in list(tmp.laser_visited_pts.values()):
            total_visited_pts += val

        if not np.any([pt not in total_visited_pts for pt in points_to_hit]):
            print('supposedly found solution')
            print(f'{config}')
            break
    end = time.perf_counter()
    print(f'elapsed time for second board solving: {end - start}')

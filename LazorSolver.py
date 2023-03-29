from Board import Board
import numpy as np
from copy import deepcopy
import time
from bffParser import openBFF


class LazorSolver:

    def __init__(self, file_ptr):
        print(f'attempting to solve {file_ptr}...')
        self.empty_board = None
        self.laser_pos_list = []
        self.laser_dir_list = []
        self.pointGoalList = None
        self.block_list = None
        self.solved_board = None
        self.unique_boards = []
        self.parse_bff(file_ptr)
        self.solve()

    def parse_bff(self, file_ptr):
        grid, laserList, pointGoalList, blockList = openBFF(file_ptr)
        self.empty_board = grid
        self.pointGoalList = pointGoalList
        self.block_list = blockList
        for laser in laserList:
            self.laser_pos_list.append(laser[0:2])
            self.laser_dir_list.append(laser[2:])

    def generate_possible_boards(self):
        possible_configs = generate_possible_configs(self.empty_board, self.block_list)
        for filled_board in possible_configs:
            b = Board(filled_board, self.laser_pos_list, self.laser_dir_list)
            self.unique_boards.append(b)

    def solve(self):
        start = time.perf_counter()
        self.generate_possible_boards()
        for board in self.unique_boards:
            board.get_laser_path()

            total_visited_pts = []
            for val in list(board.laser_visited_pts.values()):
                total_visited_pts += val

            if not np.any([pt not in total_visited_pts for pt in self.pointGoalList]):
                print('found solution')
                print(f'{board.board}')
                self.solved_board = board
                break

        end = time.perf_counter()
        if self.solved_board is None:
            print('*** could not find a solution ***')
        else:
            print(f'solved in {end - start} seconds')


def generate_possible_configs(input_empty_board, blocks_to_place):
    not_free_block_types = [4, 5, 6, 7]
    input_dims = []
    input_dims.append(len([1 for l in input_empty_board]))
    input_dims.append(len(input_empty_board[0]))
    input_dims = tuple(input_dims)

    # convert to numpy array and flatten for the recursive function call
    empty_board = np.array(input_empty_board)
    empty_board = empty_board.flatten()

    free_site_idxs = [i for i, block in enumerate(empty_board) if block not in not_free_block_types]

    possible_configs = recurse_generate_boards(empty_board, blocks_to_place, free_site_idxs)
    #print(f'board after step 1: {possible_configs[0]}')
    # convert from 1D numpy arrays to 2D nested Python lists
    possible_configs = [*set([tuple(arr) for arr in possible_configs])]
    #print(f'board after step 2: {possible_configs[0]}')
    possible_configs = [np.array(arr) for arr in possible_configs]
    #print(f'board after step 3: {possible_configs[0]}')
    possible_configs = [arr.reshape(input_dims) for arr in possible_configs]
    #print(f'board after step 4: {possible_configs[0]}')
    possible_configs = [[list(arr) for arr in sublist] for sublist in possible_configs]
    #print(f'board after step 5: {possible_configs[0]}')
    possible_configs = [list(arr) for arr in possible_configs]
    #print(f'board after step 6: {possible_configs[0]}')
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
    solver = LazorSolver('mad_4.bff')

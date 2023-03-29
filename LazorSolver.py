from Board import Board
import numpy as np
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


#@jit(nopython=True)
def generate_possible_configs(input_empty_board, blocks_to_place):
    not_free_block_types = [4, 5, 6, 7]
    input_dims = []
    input_dims.append(len([1 for l in input_empty_board]))
    input_dims.append(len(input_empty_board[0]))

    # convert to numpy array and flatten for the recursive function call
    empty_board = np.array(input_empty_board)
    empty_board = empty_board.flatten()

    free_site_idxs = [i for i, block in enumerate(empty_board) if block not in not_free_block_types]
    possible_configs = recurse_generate_boards(empty_board, blocks_to_place, free_site_idxs, placed_sites=[])
    #print('exited recurse_generate_boards call')
    #print(f'initial return has {len(possible_configs)} boards')
    #print(f'board after step 1: {possible_configs[0]}')
    # convert from 1D numpy arrays to 2D nested Python lists
    possible_configs = [*set([tuple(arr) for arr in possible_configs])]
    #print(f'board after step 2: {possible_configs[0]}')
    possible_configs = [np.array(arr) for arr in possible_configs]
    #print(f'board after step 3: {possible_configs[0]}')
    possible_configs = [arr.reshape((input_dims[0], input_dims[1])) for arr in possible_configs]
    #print(f'board after step 4: {possible_configs[0]}')
    possible_configs = [[list(arr) for arr in sublist] for sublist in possible_configs]
    #print(f'board after step 5: {possible_configs[0]}')
    possible_configs = [list(arr) for arr in possible_configs]
    #print(f'board after step 6: {possible_configs[0]}')
    #print(f'found {len(possible_configs)} unique board configs')
    return possible_configs


def recurse_generate_boards(input_board, blocks_to_place, free_site_idxs, placed_sites):
    list_of_returned_configs = []  # should only hold complete, valid board configs
    visited_blocks = []
    placed_block_types = [1, 2, 3]

    # base case: no more blocks to place, return input_board
    if len(blocks_to_place) == 0:
        list_of_returned_configs.append(list(input_board))
        return list_of_returned_configs

    for i, block in enumerate(blocks_to_place):  # for each unique block still left to place at this level
        if block in visited_blocks:
            continue

        visited_blocks.append(block)

        # for each free site where you can place this block in the input board
        for j, site in enumerate(free_site_idxs):
            # top-level filter: don't place any block of the same kind as the top level block in any site before
            # its last appearance...already covered by previous loops
            if len(placed_sites) > 0:
                sites = [z for z, placed_block in enumerate(input_board) if
                         placed_block in placed_block_types and block == placed_block]
                if len(sites) > 0 and site < sites[-1]:
                    continue

            # recursive call with updated board and lists
            updated_board = [row for row in input_board]
            updated_board[site] = block  # place the block
            updated_blocks_to_place = [block for block in blocks_to_place]
            updated_blocks_to_place.pop(i)
            updated_free_site_idxs = [site for site in free_site_idxs]
            updated_free_site_idxs.pop(j)
            updated_placed_sites = placed_sites + [site]
            received_boards = recurse_generate_boards(updated_board, updated_blocks_to_place, updated_free_site_idxs, updated_placed_sites)

            list_of_returned_configs += received_boards  # add received boards to list of boards to return

    return list_of_returned_configs


if __name__ == '__main__':
    solver = LazorSolver('dark_1.bff')

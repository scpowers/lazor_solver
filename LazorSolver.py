from Board import Board
import numpy as np
import time
from bffParser import openBFF


class LazorSolver:
    """
    A class to represent a Lazors puzzle solver, which is the high-level class that a user would instantiate.

    **Attributes**

        empty_board: *list, list, int*
            A double-nested list representing the given puzzle board with none of the placeable blocks on it
        laser_pos_list: *list, list, int*
            A double-nested list holding [x, y] coords of the laser sources
        laser_dir_list: *list, list, int*
            A double-nested list holding [vx, vy] directions of the laser sources
        pointGoalList: *list, list, int*
            A double-nested list holding [x, y] positions of the points that the laser must pass through
        blockList: *list, int*
            A list holding the blocks that must be placed using the following convention:
                1 - reflective block
                2 - refractive block
                3 - opaque block
        solved_board: *Board object*
            A Board object representing the configuration of the board when the puzzle is solved
        unique_boards: *list, Board object*
            A list of the unique Board objects returned by the method to generate unique board configurations

    **Methods**

        parse_bff: parses a .bff file from a given file pointer
            args - file_ptr (string)
            returns - None
        generate_possible_boards: generates all unique Board objects for the given blocks to place
            args - None
            returns - None
        solve: combs through the unique boards to find one whose laser path goes through all required points
            args - None
            returns - None
    """

    def __init__(self, file_ptr):
        """
        LazorSolver class constructor

        **Parameters**

            file_ptr: *str*
                A string pointing to the .bff file to solve

        **Returns**

            None
        """
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
        """
        Parse a given .bff file to extract the information needed to solve the puzzle.

        **Parameters**

            file_ptr: *str*
                A string pointing to the .bff file to solve

        **Returns**

            None
        """
        grid, laserList, pointGoalList, blockList = openBFF(file_ptr)
        self.empty_board = grid
        self.pointGoalList = pointGoalList
        self.block_list = blockList
        for laser in laserList:
            self.laser_pos_list.append(laser[0:2])
            self.laser_dir_list.append(laser[2:])

    def generate_possible_boards(self):
        """
        Generate all unique boards for the given empty board and blocks to place.

        **Parameters**

            None

        **Returns**

            None
        """
        possible_configs = generate_possible_configs(self.empty_board, self.block_list)
        for filled_board in possible_configs:
            b = Board(filled_board, self.laser_pos_list, self.laser_dir_list)
            self.unique_boards.append(b)

    def solve(self):
        """
        Comb through all generated boards to find one whose laser path goes through the required points.

        **Parameters**

            None

        **Returns**

            None
        """
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
    """
    Static method to generate boards in the simpler double-nested-list format to be converted to Board objects later.

    **Parameters**

        input_empty_board: *list, list, int*
            A double-nested list representing the empty board to solve (no free blocks placed)
        blocks_to_place: *list, int*
            A list of all blocks to place following the integer mapping in the LazorSolver class

    **Returns**

        possible_configs: *list, list, int*
            A list of double-nested lists representing the unique board configurations
    """
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
    """
    Recursive method to generate unique boards represented as double-nested lists of integers

    **Parameters**

        input_empty_board: *list, list, int*
            A double-nested list representing the empty board to solve (no free blocks placed)
        blocks_to_place: *list, int*
            A list of all blocks to place following the integer mapping in the LazorSolver class
        free_site_idxs: *list, int*
            A list of all indexes in the input board where you are allowed to place blocks
        placed_sites: *list, int*
            A list of all indexes in the input board where you already placed a block

    **Returns**

        list_of_returned_configs: *numpy.array<int, 1D>*
            A list of 1-D numpy arrays of integers representing flattened boards
    """
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

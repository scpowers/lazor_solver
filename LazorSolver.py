from Board import Board


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

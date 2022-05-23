from math import inf


def evaluate(board):
    won, who = board.won()
    if who == 'O': return 10 + board.empty()
    elif who == 'X': return -10 - board.empty()
    score = 0
    for row in board.grid:
        if row.count('O') == 2 and row.count('.'): score += 1
        if row.count('X') == 2 and row.count('.'): score -= 1
    for col in range(3):
        column = ''.join(board.grid[row][col] for row in range(3))
        if column.count('O') == 2 and column.count('.'): score += 1
        if column.count('X') == 2 and column.count('.'): score -= 1
    diagonal1 = ''.join(board.grid[rc][rc] for rc in range(3))
    if diagonal1.count('O') == 2 and diagonal1.count('.'): score += 1
    if diagonal1.count('X') == 2 and diagonal1.count('.'): score -= 1
    diagonal2 = ''.join(board.grid[rc][2 - rc] for rc in range(3))
    if diagonal2.count('O') == 2 and diagonal2.count('.'): score += 1
    if diagonal2.count('X') == 2 and diagonal2.count('.'): score -= 1
    return score


class Minimax:

    def max(self, board, depth):
        if not depth or board.is_full() or board.won()[0]:
            return evaluate(board), None
        moves = board.possible_moves()
        score = -inf
        best_move = (-1, -1)
        for move in moves:
            row, col = move
            board.insert(row, col, 'O')
            move_score, _ = self.min(board, depth - 1)
            if move_score > score:
                score = move_score
                best_move = (row, col)
            board.pop(row, col)
        return score, best_move

    def min(self, board, depth):
        if not depth or board.is_full() or board.won()[0]:
            return evaluate(board), None
        moves = board.possible_moves()
        score = inf
        worst_move = (-1, -1)
        for move in moves:
            row, col = move
            board.insert(row, col, 'X')
            move_score, _ = self.max(board, depth - 1)
            if move_score < score:
                score = move_score
                worst_move = (row, col)
            board.pop(row, col)
        return score, worst_move

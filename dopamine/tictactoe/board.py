class Board:
    grid = []
    available_moves = []

    def __init__(self):
        self.grid = [
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]
        self.available_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __str__(self):
        # Return de debugage
        # return '\n'.join(' '.join(row) for row in self.grid)
        answer = ''
        for row_nb in range(3):
            row = self.grid[row_nb]
            for col_nb in range(3):
                cell = row[col_nb]
                match cell:
                    case '.':
                        number = (2 - row_nb) * 3 + col_nb + 1
                        match number:
                            case 1: answer += ':one:'
                            case 2: answer += ':two:'
                            case 3: answer += ':three:'
                            case 4: answer += ':four:'
                            case 5: answer += ':five:'
                            case 6: answer += ':six:'
                            case 7: answer += ':seven:'
                            case 8: answer += ':eight:'
                            case 9: answer += ':nine:'
                    case 'X': answer += ':x:'
                    case 'O': answer += ':o:'
                if col_nb != 2: answer += ' | '
                elif row_nb != 2: answer += '\n'
        return answer


    def insert(self, row, col, char):
        self.grid[row][col] = char

    def pop(self, row, col):
        self.grid[row][col] = '.'

    def is_full(self):
        return '.' not in self.__str__()

    def is_filled(self, row, col):
        return self.grid[row][col] != '.'

    def empty(self):
        return self.__str__().count('.')

    def possible_moves(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.grid[row][col] == '.':
                    moves.append((row, col))
        return moves

    def won(self):
        for symbol in 'XO':
            for row in self.grid:
                if row.count(symbol) == 3: return True, symbol
            for col in range(3):
                if (''.join(self.grid[row][col] for row in range(3))).count(symbol) == 3: return True, symbol
            if ''.join(self.grid[rc][rc] for rc in range(3)).count(symbol) == 3: return True, symbol
            if ''.join(self.grid[rc][2-rc] for rc in range(3)).count(symbol) == 3: return True, symbol
        return False, ''

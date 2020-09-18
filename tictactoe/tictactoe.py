##
# author:   Jonathan Abbott
# date:     Sep 17, 2020
#
# The tictactoe game instance.

class TicTacToe:
    def __init__(self):
        self.turn = 'X'
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-'],
        ]
        self.winner = ''
    
    def invalid_spot(self, row: int, col: int) -> bool:
        if row < 0 or len(self.board) <= row:
            return True
        if col < 0 or len(self.board[0]) <= col:
            return True
        if self.board[row][col] != '-':
            return True
        return False

    def game_over(self) -> bool:
        return self.winner != ''
    
    def winning_move(self, row: int, col: int) -> bool:
        # Check \
        backdiag = True
        for i in range( len(self.board) ): # This assumes a square board.
            backdiag = backdiag and self.board[i][i] == self.turn
        if backdiag: return True
        
        # Check /
        frontdiag = True
        for i in range( len(self.board) ):
            frontdiag = frontdiag and self.board[-1 - i][i] == self.turn
        if frontdiag: return True

        # Check horizontals.
        for row in range( len(self.board) ):
            horiz = True
            for col in range( len(self.board[row]) ):
                horiz = horiz and self.board[row][col] == self.turn
            if horiz: return True
        
        # Check verticals.
        for col in range( len(self.board[0]) ):
            vert = True
            for row in range( len(self.board) ):
                vert = vert and self.board[row][col] == self.turn
            if vert: return True
        
        return False


    def move(self, row: int, col: int) -> bool:
        if self.invalid_spot(row, col):
            return False
        self.board[row][col] = self.turn
        if self.winning_move(row, col):
            self.winner = self.turn
            return False
        if self.turn == 'X': self.turn = 'O'
        else: self.turn = 'X'
        return True
    

    def __str__(self):
        return f'''Send in your move as two comma-delimited values.
It is {self.turn}'s turn.
{' '.join(self.board[0])}
{' '.join(self.board[1])}
{' '.join(self.board[2])}
{f'{self.winner} has won!' if self.winner else ''}
'''
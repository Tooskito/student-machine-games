
class Game:

    def disable_requests_if_game_over(fn):
        def wrapper(self, request):
            if self.game_over():
                return self.__str__()
            else:
                return fn(self, request)
        wrapper.__name__ = 'disable-requests-wrapper'
        return wrapper
    
    def __init__(self):
        self.turn = 'X'
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-'],
        ]
        self.left = len(self.board) * len(self.board[0])
        self.winner = ''
    
    def game_over(self) -> bool:
        return self.winner != ''
    
    def invalid_spot(self, row: int, col: int) -> bool:
        if row < 0 or len(self.board) <= row: return True
        if col < 0 or len(self.board[0]) <= col: return True
        if self.board[row][col] != '-': return True
        return False
    
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
        if self.invalid_spot(row, col): return False
        self.board[row][col] = self.turn
        self.left -= 1
        if self.winning_move(row, col):
            self.winner = self.turn
            return False
        if self.turn == 'X': self.turn = 'O'
        else: self.turn = 'X'
        return True
    
    @disable_requests_if_game_over
    def process_request(self, request):
        request = [unstripped_index.strip() for unstripped_index in request.split(',')]
        response = str()
        try:
            row, col = int(request[0]), int(request[1])
            self.move(row, col)
            response = self.__str__()
        except ValueError:
            response = 'could not parse indices.\n'
        except IndexError:
            response = 'invalid request.\n'
        return response

    def __str__(self):
        return f'''It is {self.turn}'s turn.
{' '.join(self.board[0])}
{' '.join(self.board[1])}
{' '.join(self.board[2])}
{f'{self.winner} has won!' if self.winner else ''}
{f'no one won :(' if self.left == 0 else ''}
'''

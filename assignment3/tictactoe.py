# tictactoe.py

class TictactoeException(Exception):
    """Custom exception class for TicTacToe game."""
    
    def __init__(self, message):
        """Initialize with a custom message."""
        self.message = message
        super().__init__(self.message)


class Board:
    """TicTacToe board class."""
    
    # Class variable for valid moves
    valid_moves = ["upper left", "upper center", "upper right", 
                   "middle left", "center", "middle right", 
                   "lower left", "lower center", "lower right"]
    
    def __init__(self):
        """Initialize a 3x3 board with empty spaces."""
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"
    
    def __str__(self):
        """Convert the board to a displayable string."""
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)
    
    def move(self, move_string):
        """Make a move on the board."""
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3  # row
        column = move_index % 3  # column
        
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        
        self.board_array[row][column] = self.turn
        self.last_move = move_string
        
        # Switch turns
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    
    def whats_next(self):
        """Check if the game is over and return status."""
        # Check if board is full (Cat's game)
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                    break
            if not cat:
                break
        
        win = False
        winner = ""
        
        # Check rows
        for i in range(3):
            if self.board_array[i][0] != " ":
                if (self.board_array[i][0] == self.board_array[i][1] and 
                    self.board_array[i][1] == self.board_array[i][2]):
                    win = True
                    winner = self.board_array[i][0]
                    break
        
        # Check columns
        if not win:
            for i in range(3):
                if self.board_array[0][i] != " ":
                    if (self.board_array[0][i] == self.board_array[1][i] and 
                        self.board_array[1][i] == self.board_array[2][i]):
                        win = True
                        winner = self.board_array[0][i]
                        break
        
        # Check diagonals
        if not win:
            if self.board_array[1][1] != " ":
                # Main diagonal
                if (self.board_array[0][0] == self.board_array[1][1] and 
                    self.board_array[2][2] == self.board_array[1][1]):
                    win = True
                    winner = self.board_array[1][1]
                # Anti-diagonal
                elif (self.board_array[0][2] == self.board_array[1][1] and 
                      self.board_array[2][0] == self.board_array[1][1]):
                    win = True
                    winner = self.board_array[1][1]
        
        if win:
            return (True, f"{winner} has won")
        elif cat:
            return (True, "Cat's Game")
        else:
            return (False, f"{self.turn}'s turn")


if __name__ == "__main__":
    print("Welcome to TicTacToe!")
    print("Valid moves:", ", ".join(Board.valid_moves))
    print()
    
    board = Board()
    
    while True:
        print(board)
        game_over, message = board.whats_next()
        
        if game_over:
            print(message)
            break
        
        print(message)
        move = input("Enter your move: ").strip()
        
        try:
            board.move(move)
        except TictactoeException as e:
            print(f"Error: {e.message}")
            print("Please try again.")
            print()
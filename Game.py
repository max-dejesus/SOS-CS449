
# Game class (may move to another file)
class Game():
    def __init__(self, boardsize = 3):
        # Initialize all game variables
        self.board_size = boardsize
        self.turn = 1
        self.piece = 'S'
        self.p1_score = 0
        self.p2_score = 0
        # Type 0 = simple, type 1 = general
        self.gametype = 0
        # Type 0 = user vs user, type 1 = user vs com, type 2 = recording/replay
        self.playertype = 0
        self.board = self.create_board(self.board_size)
        # Flag for game state
        self.active_game = False
    
    #region Getters / setters
    def get_board(self):
        return self.board
    def get_board_size(self):
        return self.board_size
    def get_p1_score(self):
        return self.p1_score
    def get_p2_score(self):
        return self.p2_score
    def get_gametype(self):
        return self.gametype
    def get_playertype(self):
        return self.gametype
    def get_piece(self):
        return self.piece
    def get_turn(self):
        return self.turn
    def set_piece(self, p):
        self.piece = p
    def set_gametype(self, t):
        self.gametype = t
    def set_playertype(self, t):
        self.playertype = t
    def set_board_size(self, s):
        self.board_size = s
    #endregion
    
    # Create board of x size and return
    def create_board(self, size):
        board = [[' '] * size for _ in range(size)]
        return board
    
    
    # Initialize a new game instance
    def new_game(self):
        self.active_game = True
        
        self.board = self.create_board(self.board_size)
        
        self.swap_turn()
        
        # TODO: add game init
        # Set board size, gametype, and player type
        # Draw correct board size to screen and begin accepting user input
        
    # Terminate a game instance
    def end_game(self):
        self.active_game = False
        
        # TODO: add end game func
        # Display score and game winner
        # Pop-up box with winner and OK button
        # After a game ends, assume program is being "reset"
        # Behave as if a new window had opened (run constructor)
    
    # Make a game move
    def move(self, r, c):
        try:
            self.board[r][c] = self.piece
            return True
        except:
            return False
    
    # Check for an SOS
    # TODO: Implement game logic
    def check_sos(self):
        return True
    
    # Score-related functions
    def inc_p1_score(self):
        try:
            self.p1_score += 1
            return True
        except:
            return False
    def inc_p2_score(self):
        try:
            self.p2_score += 1
            return True
        except:
            return False
    
    # Swap current turn
    def swap_turn(self):
        if self.turn == 1: self.turn = 2
        else: self.turn = 1
# SOS Game class
# Entirely encapsulated. This class will NOT handle any errors, anything that is passed into its functions will be assumed to be correct.
# Errors are to be handled by the GUI or other user interface

class Game():
    # Constructor
    def __init__(self, boardsize = 3):
        # Initialize all game variables
        self._board_size = boardsize
        self._turn = 1
        self._piece = 'S'
        self._p1_score = 0
        self._p2_score = 0
        # Type 0 = simple, type 1 = general
        self._gametype = 0
        # Type 0 = user vs user, type 1 = user vs com, type 2 = recording/replay TODO
        self._playertype = 0
        self._board = self.create_board(self._board_size)
        # Flag for game state
        self._active_game = False
    
    #region Getters / setters
    def get_board(self):
        return self._board
    def get_board_size(self):
        return self._board_size
    def get_p1_score(self):
        return self._p1_score
    def get_p2_score(self):
        return self._p2_score
    def get_gametype(self):
        return self._gametype
    def get_playertype(self):
        return self._gametype
    def get_piece(self):
        return self._piece
    def get_turn(self):
        return self._turn
    def is_active(self):
        return self._active_game
    def set_piece(self, p):
        self._piece = p
    def set_gametype(self, t):
        self._gametype = t
    def set_playertype(self, t):
        self._playertype = t
    def set_board_size(self, s):
        self._board_size = s
    #endregion
    
    # Create board of x size and return
    def create_board(self, size):
        board = [[' '] * size for _ in range(size)]
        return board
    
    # Initialize a new game instance
    def new_game(self):
        self._active_game = True
        self._turn = 1
        self._board = self.create_board(self._board_size)
        
    # Terminate a game instance
    def end_game(self, winner):
        self._active_game = False
        
        # TODO: add end game func
        # Display score and game winner
        # Pop-up box with winner and OK button
        # After a game ends, assume program is being "reset"
        # Behave as if a new window had opened (run constructor)
    
    # Score incrementer
    def inc_score(self):
        if self._turn == 1: self._p1_score += 1
        else: self._p2_score += 1
    
    # Swap current turn
    def swap_turn(self):
        if self._turn == 1: self._turn = 2
        else: self._turn = 1
        
    # Make a game move
    def move(self, r, c):
        try:
            self._board[r][c] = self._piece
            if self.check_sos(r, c):
                self.inc_score()
            else: pass
            if self.is_won():
                self.end_game()
            else:
                self.swap_turn()
                return True
        except:
            return False
    
    # Check for an SOS
    # TODO: Implement game logic
    # Design notes: 
    # O piece needs to check 0-4 neighbors based on whether or not it is touching 0 edges, 1 edge, or 2 edges
    # S piece needs to check 3-8 neighbors based on the same idea
    # O piece will have 0 valid neighbors for scoring if touching 2 edges
    # O piece will have 1 valid neighbors for scoring if touching 1 edge
    # O piece will have 4 valid neighbors for scoring if touching no edge
    # S piece will have 3 valid neighbors for scoring if touching 2 edges
    # S piece will have 5 valid neighbors for scoring if touching 1 edge
    # S piece will have 8 valid neighbors for scoring if touching no edge
    def check_sos(self, r, c):
        '''
        def edges_touched(self):
            edges = 0
            if r == 0 or r == (self._board_size - 1):
                edges += 1
            if c == 0 or c == (self._board_size - 1):
                edges += 1
            return edges
        
        match self._piece:
            case 'S':
                return
            case "O":
                if edges_touched() == 2:
                    return False
                if edges_touched() == 1:
                    #TODO: implement
                    pass
        '''
        return
    
    # TODO: Determine if the game is "won" based on gamemode
    # Win in simple if any player gets an SOS
    # Win in general if board is filled, winner is player w/ most points
    def is_won(self):
        if self._gametype == 0:
            if self._p1_score > 0 or self._p2_score > 0:
                return True
            else:
                return False
        else:
            for ls in self._board:
                if ' ' in ls:
                    return False
            return True
    
    

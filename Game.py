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
        self._no_moves = 0
        # Type 0 = simple, type 1 = general
        self._gametype = 0
        # Type 0 = user vs user, type 1 = user vs COM, type 2 = COM v COM, type 3 = recording/replay
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
    def get_no_moves(self):
        return self._no_moves
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
        self._p1_score = 0
        self._p2_score = 0
        self._no_moves = 0
        self._board = self.create_board(self._board_size)
        
    # Terminate a game instance
    def end_game(self):
        self._active_game = False
        if self._p1_score > self._p2_score:
            return 1
        elif self._p1_score < self._p2_score:
            return 2
        else: 
            return False
        
    # Score incrementer, default 1 but optionally allows increase by input integer
    def inc_score(self, c = 1):
        if self._turn == 1: self._p1_score += c
        else: self._p2_score += c
    
    # Swap current turn
    def swap_turn(self):
        if self._turn == 1: self._turn = 2
        else: self._turn = 1
        
    # Make a game move
    def move(self, r, c):
        try:
            self._board[r][c] = self._piece
            self._no_moves += 1
        except:
            return False
    
    # Check for an SOS
    # Design notes: 
    # O piece needs to check 0-4 neighbors based on whether or not it is touching 0 edges, 1 edge, or 2 edges
    # S piece needs to check 3-8 neighbors based on the same idea
    # O piece will have 0 valid neighbors for scoring if touching 2 edges - done
    # O piece will have 1 valid neighbors for scoring if touching 1 edge - done
    # O piece will have 4 valid neighbors for scoring if touching no edge - done
    # S piece will have 3 valid neighbors for scoring if touching 2 edges - done
    # S piece will have 5 valid neighbors for scoring if touching 1 edge - done
    # S piece will have 8 valid neighbors for scoring if touching no edge - done
    def check_sos(self, r, c):
        # Inner function returns string of what edges the given coordinate touches.
        # Useful for determining how many neighbors to test against or determining escape conditions early.
        def edges_touched(r,c):
            edges = ''
            if r == 0:
                edges += 'N'
            elif r == (self._board_size - 1):
                edges += 'S'
            if c == 0:
                edges += 'W'
            elif c == (self._board_size - 1):
                edges += 'E'
            return edges
        
        edges = edges_touched(r,c)
        soses = []
        
        match self._piece:
            case 'S':
                if len(edges) == 2:
                    match edges:
                        case 'NW' | 'NE':
                            if edges == 'NW':
                                n1 = 1
                                n2 = 2
                            elif edges == 'NE':
                                n1 = -1
                                n2 = -2
                            
                            if self._board[r][c+n1] == 'O':
                                if self._board[r][c+n2] == 'S':
                                    soses.append((r,c))
                                    soses.append((r,c+n2))
                            if self._board[r+1][c] == 'O':
                                if self._board[r+2][c] == 'S':
                                    soses.append((r,c))
                                    soses.append((r+2,c))
                            if self._board[r+1][c+n1] == 'O':
                                if self._board[r+2][c+n2] == 'S':
                                    soses.append((r,c))
                                    soses.append((r+2,c+n2))
                        case 'SW' | 'SE':
                            if edges == 'SW':
                                n1 = 1
                                n2 = 2
                            elif edges == 'SE':
                                n1 = -1
                                n2 = -2
                            
                            if self._board[r][c+n1] == 'O':
                                if self._board[r][c+n2] == 'S':
                                    soses.append((r,c))
                                    soses.append((r,c+n2))
                            if self._board[r-1][c] == 'O':
                                if self._board[r-2][c] == 'S':
                                    soses.append((r,c))
                                    soses.append((r-2,c))
                            if self._board[r-1][c+n1] == 'O':
                                if self._board[r-2][c+n2] == 'S':
                                    soses.append((r,c))
                                    soses.append((r-2,c+n2))
                elif len(edges) == 1:
                    match edges:
                        case 'N' | 'S':
                            nghbr_r = r
                            nghbr_c = c - 1
                            
                            if edges == 'N':
                                dr = 1
                            elif edges == 'S':
                                dr = -1
                                
                            # Tests above/below rows for possible valid SOS
                            while nghbr_c <= c+1:
                                nghbr_edges = edges_touched(nghbr_r, nghbr_c)
                                if len(nghbr_edges) > len(edges):
                                    pass
                                else:
                                    if nghbr_c == c-1:
                                        dc = -1
                                    elif nghbr_c == c+1:
                                        dc = 1

                                    if self._board[nghbr_r][nghbr_c] == 'O':
                                        if self._board[nghbr_r][nghbr_c+dc] == 'S':
                                            soses.append((r,c))
                                            soses.append((nghbr_r,nghbr_c+dc))
                                    if self._board[nghbr_r+dr][nghbr_c] == 'O':
                                        if self._board[nghbr_r+dr+dr][nghbr_c+dc] == 'S':
                                            soses.append((r,c))
                                            soses.append((nghbr_r+dr+dr,nghbr_c+dc))
                                nghbr_c += 2
                           
                            # Tests left/right cell for possible valid SOS
                            if self._board[r+dr][c] == 'O':
                                if self._board[r+dr+dr][c] == 'S':
                                    soses.append((r,c))
                                    soses.append((r+dr+dr,c))     
                        case 'W' | 'E':
                            nghbr_r = r - 1
                            nghbr_c = c
                            
                            if edges == 'W':
                                dc = 1
                            elif edges == 'E':
                                dc = -1
                            
                            # Tests left/right cols for possible valid SOS
                            while nghbr_r <= r+1:
                                nghbr_edges = edges_touched(nghbr_r, nghbr_c)
                                if len(nghbr_edges) > len(edges):
                                    pass
                                else:
                                    if nghbr_r == r-1:
                                        dr = -1
                                    elif nghbr_r == r+1:
                                        dr = 1

                                    if self._board[nghbr_r][nghbr_c] == 'O':
                                        if self._board[nghbr_r+dr][nghbr_c] == 'S':
                                            soses.append((r,c))
                                            soses.append((nghbr_r+dr,nghbr_c))
                                    if self._board[nghbr_r][nghbr_c+dc] == 'O':
                                        if self._board[nghbr_r+dr][nghbr_c+dc+dc] == 'S':
                                            soses.append((r,c))
                                            soses.append((nghbr_r+dr,nghbr_c+dc+dc))
                                nghbr_r += 2         

                            # Tests above/below cell for possible valid SOS
                            if self._board[r][c+dc] == 'O':
                                if self._board[r][c+dc+dc] == 'S':
                                    soses.append((r,c))
                                    soses.append((r,c+dc+dc))
                elif len(edges) == 0:
                    nghbr_r = r - 1
                    nghbr_c = c - 1
                    
                    # Check rows above/below for possible valid SOS
                    while nghbr_r <= r+1:
                        while nghbr_c - c < 2:
                            nghbr_edges = edges_touched(nghbr_r, nghbr_c)
                            if len(nghbr_edges) == 2:
                                break # Always fails, move to next row
                            elif len(nghbr_edges) == 1:
                                nghbr_c += 1
                                continue # Invalid, but move to next col
                            else:
                                dr = nghbr_r - r
                                dc = nghbr_c - c
                                
                                if self._board[nghbr_r][nghbr_c] == 'O':
                                    if self._board[nghbr_r+dr][nghbr_c+dc] == 'S':
                                        soses.append((r,c))
                                        soses.append((nghbr_r+dr, nghbr_c+dc))
                            nghbr_c += 1            
                        nghbr_r += 2
                        nghbr_c = c-1
                    
                    # Check left/right cell for possible valid SOS
                    nghbr_r = r
                    nghbr_c = c-1
                    while nghbr_c - c < 2:
                        nghbr_edges = edges_touched(nghbr_r, nghbr_c)
                        if len(nghbr_edges) > 0:
                            nghbr_c += 2
                            continue
                        else:
                            dc = nghbr_c - c
                            if self._board[nghbr_r][nghbr_c] == 'O':
                                if self._board[nghbr_r][nghbr_c+dc] == 'S':
                                    soses.append((r,c))
                                    soses.append((nghbr_r, nghbr_c+dc))
                            nghbr_c += 2       
            case "O":
                if len(edges) == 2:
                    # Automatically knows that state is false
                    pass
                elif len(edges) == 1:
                    match edges:
                        case 'N' | 'S':
                            # Check left neighbor first, then right. If both are S, add coords to SOSes list
                            if self._board[r][c-1] == 'S':
                                if self._board[r][c+1] == 'S':
                                    soses.append((r, c-1))
                                    soses.append((r, c+1))
                            else:
                                pass
                        case 'E' | 'W':
                            # Check top neighbor first, then bottom. If both are S, add coords to SOSes list
                            if self._board[r-1][c] == 'S':
                                if self._board[r+1][c] == 'S':
                                    soses.append((r-1, c))
                                    soses.append((r+1, c))
                            else:
                                pass
                elif len(edges) == 0:
                    # Set neighbor row/col vars, starts at r-1, c-1 (top left of current r,c)
                    nghbr_r = r - 1
                    nghbr_c = c - 1
                    
                    # Whole set of loops will run four times TOTAL
                    while nghbr_r != r + 1:
                        while nghbr_c - c < 2:
                            if self._board[nghbr_r][nghbr_c] == 'S':
                                if nghbr_r == r-1 and nghbr_c == c-1:
                                    if self._board[nghbr_r+2][nghbr_c+2] == 'S':
                                        soses.append((nghbr_r, nghbr_c))
                                        soses.append((nghbr_r+2, nghbr_c+2))
                                elif nghbr_r == r-1 and nghbr_c == c:
                                    if self._board[nghbr_r+2][nghbr_c] == 'S':
                                        soses.append((nghbr_r, nghbr_c))
                                        soses.append((nghbr_r+2, nghbr_c))
                                elif nghbr_r == r-1 and nghbr_c == c+1:
                                    if self._board[nghbr_r+2][nghbr_c-2] == 'S':
                                        soses.append((nghbr_r, nghbr_c))
                                        soses.append((nghbr_r+2, nghbr_c-2))
                                elif nghbr_r == r and nghbr_c == c-1:
                                    if self._board[nghbr_r][nghbr_c+2] == 'S':
                                        soses.append((nghbr_r, nghbr_c))
                                        soses.append((nghbr_r, nghbr_c+2))
                            elif nghbr_r == r:
                                break
                            nghbr_c += 1
                            
                        nghbr_c = c - 1
                        nghbr_r += 1
                   
        if len(soses) == 0:
            return False
        else: 
            return soses
                        
                        
    # Determine if the game is "won" based on gamemode
    # Win in simple (gametype 0) if any player gets an SOS
    # Win in general (gametype 1) if board is filled, winner is player w/ most points
    def is_won(self):
        if self._gametype == 0:
            if self._p1_score > 0 or self._p2_score > 0:
                return True
            else:
                for ls in self._board:
                    if ' ' in ls:
                        return False
                return True
        elif self._gametype == 1:
            for ls in self._board:
                if ' ' in ls:
                    return False
            return True
    
if __name__ == '__main__':
    print("DEBUG")
    game_inst = Game(5)
    print('Game instance created')
    r = 1
    c = 1
    game_inst.set_piece('O')
    game_inst.move(1,2)
    game_inst.move(2,2)
    game_inst.set_piece('S')
    game_inst.move(1,3)
    game_inst.move(3,3)
    
    game_inst.set_piece('S')

    print('Run Check SOS, params r', r, 'c', c)
    print(game_inst.check_sos(r,c))
    

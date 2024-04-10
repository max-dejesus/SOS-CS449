from random import random, choice, randint
from Game import Game
from time import perf_counter_ns

class COM():
    # Constructor
    def __init__(self, game: Game):
        self.player = choice((1, 2))
        self.game = game
        self.zero_moves = []
        self.one_moves = []
        self.two_moves = []
        self.three_plus_moves = []
        self.last_move = ()
        self.last_piece = ''
    
    #region Getters / setters
    def get_last_move(self):
        return self.last_move
    def get_last_piece(self):
        return self.last_piece
    def get_player(self):
        return self.player
    def set_player(self, p):
        self.player = p
    #endregion
        
    # Determine and weigh possible moves
    def get_moves(self):
        bs = self.game.get_board_size()
        board = self.game.get_board()
        
        if self.game.get_no_moves() == 0:
            r = randint(0, bs-1)
            c = randint(0, bs-1)
            piece = choice(('S', 'O'))
            self.zero_moves.append(((r,c), piece))
        elif self.game.get_no_moves() == 1:
                while True:
                    r = randint(0, bs-1)
                    c = randint(0, bs-1)
                    if board[r][c] != ' ':
                        continue
                    else:
                        break
                piece = choice(('S', 'O'))
                self.zero_moves.append(((r,c), piece)) 
        else:
            piece = 'S'
            count = 0
            while count != 2:
                self.game.set_piece(piece)
                for r in range(bs):
                    for c in range(bs):
                        if board[r][c] != ' ':
                            continue
                        else:
                            soses = self.game.check_sos(r,c)
                            if soses:
                                if len(soses) == 2:
                                    self.one_moves.append(((r,c), piece))
                                elif len(soses) == 4:
                                    self.two_moves.append(((r,c), piece))
                                elif len(soses) > 4:
                                    self.three_plus_moves.append(((r,c), piece))
                            else:
                                self.zero_moves.append(((r,c), piece))
                piece = 'O'
                count += 1
        
        return  
      
    # Select best move, perform, and update vars
    def select_move(self):
        pf_start = perf_counter_ns()
        self.get_moves()
        pf_end = perf_counter_ns()
        #print("COM get_moves executed. Time elapsed: ", pf_end-pf_start, 'ns')
        mutator = random()
        if mutator < 0.05:
            print('Mutated!')
        if self.three_plus_moves:
            if mutator < 0.05:
                move, piece = choice(self.zero_moves)
            move, piece = choice(self.three_plus_moves)
        elif self.two_moves:
            if mutator < 0.05:
                move, piece = choice(self.zero_moves)
            move, piece = choice(self.two_moves)
        elif self.one_moves:
            if mutator < 0.05:
                move, piece = choice(self.zero_moves)
            move, piece = choice(self.one_moves)
        else:
            move, piece = choice(self.zero_moves)
        # Empty out move lists
        self.zero_moves.clear()
        self.one_moves.clear()
        self.two_moves.clear()
        self.three_plus_moves.clear()
        
        self.last_move = move
        self.last_piece = piece
        return (move, piece)

if __name__ == "__main__":
    print('DEBUG')
    game = Game()
    com = COM(game)
    game.new_game()
    
    # Move 1, true random
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
    
    # Move two, random excluding already placed piece
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
    
    # Move three, starts checking SOSes and finding good moves
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
    
    # Move 4
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
    
    # Move 5
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
    
    # Move 6
    move, pc = com.select_move()
    game.set_piece(pc)
    game.move(move[0], move[1])
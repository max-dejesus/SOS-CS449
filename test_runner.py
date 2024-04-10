import unittest
import sys, os
from Game import Game
from main import App
from COM import COM

# Functions to revoke/restore printing operations
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

# Class for any Game class related test cases
class TestGameClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sample = Game(5)
        
    # Test A1: Game class board creation
    def test_board_creation(self):
        blockPrint()
        example = [[' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],  
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(self.sample.get_board(), example)
        enablePrint()
        print("test a1 passed")
    
    # Test A2: Game class piece move/addition
    def test_move(self):
        blockPrint()
        example = [[' ', ' ', ' ', ' ', ' '],
                        [' ', 'S', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ']]
        self.sample.set_piece('S')
        self.sample.move(1, 1)
        self.assertEqual(self.sample.get_board(), example)
        enablePrint()
        print('test a2 passed')
    
    # Test A3: Game class start a new game
    def test_new_game(self):
        blockPrint()
        bs = 6
        self.sample.set_board_size(bs)
        self.sample.new_game()
        self.assertEqual(True, self.sample.is_active())
        self.assertEqual(len(self.sample.get_board()), bs)
        self.assertEqual(len(self.sample.get_board()[0]), bs)
        enablePrint()
        print('test a3 passed')
    
    # Test A4: Game class check SOS case 1
    def test_check_sos(self):
        blockPrint()
        bs = 4
        self.sample.set_board_size(bs)
        self.sample.new_game()
        # With pieces at given position, evaluate check_sos on next piece pos and get correct response
        self.sample.set_piece('S')
        self.sample.move(3,2)
        self.sample.set_piece('O')
        self.sample.move(2,1)
        self.sample.set_piece('S')
        
        test = [(1,0), (3,2)]
        actual = self.sample.check_sos(1,0)
        
        self.assertEqual(test, actual)
        enablePrint()
        print('test a4 passed')
    
    # Test A5: do some sample moves (taken from A4) and check the win conditions for simple game
    def test_simple_win(self):
        blockPrint()
        bs = 4
        self.sample.set_board_size(bs)
        self.sample.set_gametype(0) # Simple gamemode
        self.sample.new_game()
        
        self.sample.set_piece('S')
        self.sample.move(3,2)
        soses = self.sample.check_sos(3,2)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.swap_turn()
        
        self.sample.set_piece('O')
        self.sample.move(2,1)
        soses = self.sample.check_sos(2,1)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.swap_turn()
        
        self.sample.set_piece('S')
        self.sample.move(1,0)
        soses = self.sample.check_sos(1,0)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
            
        self.assertEqual(False, self.sample.is_active())
        enablePrint()
        print('Test a5 passed')
        
    # Test A6: general game win conditions and game termination
    def test_general_win(self):
        blockPrint()
        bs = 3
        self.sample.set_board_size(bs)
        self.sample.set_gametype(1) # General gamemode
        self.sample.new_game()
        
        self.sample.set_piece('S')
        self.sample.move(2,2)
        soses = self.sample.check_sos(2,2)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.swap_turn()
        
        self.sample.set_piece('O')
        self.sample.move(1,1)
        soses = self.sample.check_sos(1,1)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.swap_turn()
        
        self.sample.set_piece('S')
        self.sample.move(0,0)
        soses = self.sample.check_sos(0,0)
        if soses:
            self.sample.inc_score()
        if self.sample.is_won():
            self.sample.end_game()
        
        self.sample.set_piece('S')
        self.sample.move(0,1)
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.set_piece('S')
        self.sample.move(0,2)
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.set_piece('S')
        self.sample.move(1,0)
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.set_piece('S')
        self.sample.move(1,2)
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.set_piece('S')
        self.sample.move(2,0)
        if self.sample.is_won():
            self.sample.end_game()
        self.sample.set_piece('S')
        self.sample.move(2,1)
        if self.sample.is_won():
            self.sample.end_game()
        
        self.assertEqual(False, self.sample.is_active())
        enablePrint()
        print('Test a6 passed')
            
# Class for any App class related test cases
class TestAppClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.app = App()
    
    # Test B1: App class board creation
    def test_board_creation(self):
        blockPrint()
        boardsize = 6
        board_v_expected_len = 36
        self.app.boardsize_v.set(boardsize)
        self.app.new_game()
        self.assertEqual(board_v_expected_len, len(self.app.board_v))
        enablePrint()
        print('test b1 passed')
        
    # Test B2: App class sends a move request to Game class
    def test_move(self):
        blockPrint()
        boardsize = 4
        example = [[' ', ' ', ' ', ' '],
                        [' ', 'O', ' ', ' '],
                        [' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ']]
        self.app.boardsize_v.set(boardsize)
        self.app.piece_v.set('O')
        self.app.new_game()
        self.app.update_board(list(self.app.board_v)[5])
        self.assertEqual(example, self.app.game.get_board())
        enablePrint()
        print('test b2 passed')

# Class for any COM class related test cases
class TestCOMClass(unittest.TestCase):
    def __init__(self, methodName: str = 'runTest') -> None:
        super().__init__(methodName)
        self.game = Game(3)
        self.com = COM(self.game)
        
    # Test C1: COM opponenet makes the first move
    def test_first_move(self):
        self.game.new_game()
        self.com.set_player(1)
        mv, pc = self.com.select_move()
        self.game.set_piece(pc)
        self.game.move(mv[0], mv[1])
        
        self.assertEqual(1, self.game.get_no_moves())
        
        print('test C1 passed')
        self.game.end_game()
        
    # Test C2: COM opponent completes an SOS and scores a point
    def test_ideal_move(self):
        self.game.new_game()
        self.com.set_player(2)
        self.game.set_piece('S')
        self.game.move(1,0)
        self.game.move(1,2)
        self.game.swap_turn()
        
        mv, pc = self.com.select_move()
        self.game.set_piece(pc)
        self.game.move(mv[0], mv[1])
        
        soses = self.game.check_sos(mv[0], mv[1])
        if soses:
            self.game.inc_score()
        
        self.assertEqual(1, self.game.get_p2_score())
        
        print('Test C2 passed')
        self.game.end_game()
    
    # Test C3: COM player finishes a general game (all spaces are filled)
    def test_game_finish(self):
        self.game.set_gametype(1) # general game
        self.game.new_game()
        self.com.set_player(1)
        moves = self.game.get_no_moves()
        
        while moves < 9:
            mv, pc = self.com.select_move()
            self.game.set_piece(pc)
            self.game.move(mv[0], mv[1])
            
            moves = self.game.get_no_moves()
        
        self.assertEqual(True, self.game.is_won())
        
        print('Test C3 passed')
        self.game.end_game()

if __name__ == '__main__':
    unittest.main()
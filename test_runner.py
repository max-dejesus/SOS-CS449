import unittest
import sys, os
from Game import Game
from main import App

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


class TestGameClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sample = Game(5)
        
    # Test 1: Game class board creation
    def test_board_creation(self):
        blockPrint()
        example = [[' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(self.sample.get_board(), example)
        enablePrint()
        print("test 1 passed")
    
    # Test 2: Game class piece move/addition
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
        print('test 2 passed')
    
    # Test 3: Game class start a new game
    def test_new_game(self):
        blockPrint()
        bs = 6
        self.sample.set_board_size(bs)
        self.sample.new_game()
        self.assertEqual(True, self.sample.is_active())
        self.assertEqual(len(self.sample.get_board()), bs)
        self.assertEqual(len(self.sample.get_board()[0]), bs)
        enablePrint()
        print('test 3 passed')
    
class TestAppClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.app = App()
    
    # Test 4: App class board creation
    def test_board_creation(self):
        blockPrint()
        boardsize = 6
        board_v_expected_len = 36
        self.app.boardsize_v.set(boardsize)
        self.app.new_game()
        self.assertEqual(board_v_expected_len, len(self.app.board_v))
        enablePrint()
        print('test 4 passed')
        
    # Test 5: App class sends a move request to Game class
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
        print('test 5 passed')

if __name__ == '__main__':
    unittest.main()
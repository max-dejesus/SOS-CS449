import unittest
from Game import Game
from main import App

class TestGameClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sample = Game(5)
        
    def test_board_creation(self):
        self.example = [[' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ']]
        self.assertEqual(self.sample.get_board(), self.example)
    
    def test_move(self):
        self.example = [[' ', ' ', ' ', ' ', ' '],
                        [' ', 'S', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ']]
        self.sample.set_piece('S')
        self.sample.move(1, 1)
        self.assertEqual(self.sample.get_board(), self.example)
    
class TestAppClass(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        app = App()

if __name__ == '__main__':
    unittest.main()
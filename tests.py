import unittest
import logic


class Tests(unittest.TestCase):
    # Test a case where x is winner
    def test_get_winner_X(self):
        board = [
            [None, None, 'O'],
            ['X', 'X', 'X'],
            [None, 'O', None],
        ]

        self.assertEqual(logic.check_win(board, 'X'), 'X')
    
    # Test a case where O is winner
    def test_get_winner_O(self):
        board = [
            ['O', 'X', 'X'],
            ['O', 'X', None],
            ['O', 'O', 'X'],
        ]

        self.assertEqual(logic.check_win(board, 'O'), 'O')
    

    # Test a case where there is stalemate
    def test_draw(self):
        board = [
            ['O', 'O', 'X'],
            ['X', 'X', 'O'],
            ['O', 'O', 'X'],
        ]
        
        self.assertEqual(logic.check_win(board, 'X'), None)

if __name__ == '__main__':
    unittest.main()
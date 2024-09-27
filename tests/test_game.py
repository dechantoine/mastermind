import unittest
from src.game import MasterMind, generate_code, check_code


class TestMasterMind(unittest.TestCase):

    def test_initialization(self):
        game = MasterMind(n_colors=6, len_code=4, n_rounds=10)
        self.assertEqual(game.n_colors, 6)
        self.assertEqual(game.len_code, 4)
        self.assertEqual(game.n_rounds, 10)
        self.assertEqual(len(game.code), 4)

        # Test initialization with code
        code = [1, 2, 3, 4]
        game = MasterMind(n_colors=6, len_code=4, n_rounds=10, code=code)
        self.assertEqual(game.code, code)

        # Test initialization with wrong length code
        code = [1, 2, 3]
        with self.assertRaises(ValueError):
            game = MasterMind(n_colors=6, len_code=4, n_rounds=10, code=code)

        # Test initialization with out of range colors
        code = [1, 2, 3, 6]
        with self.assertRaises(ValueError):
            game = MasterMind(n_colors=6, len_code=4, n_rounds=10, code=code)

    def test_generate_code(self):
        game = MasterMind(n_colors=6, len_code=4, n_rounds=10)
        generate_code()
        self.assertEqual(len(game.code), 4)
        self.assertTrue(all(0 <= color < 6 for color in game.code))

    def test_check_code(self):
        code = [1, 2, 3, 4]

        # Test correct guess
        guess = [1, 2, 3, 4]
        right_positions, wrong_positions = check_code(guess, code)
        self.assertEqual(right_positions, 4)
        self.assertEqual(wrong_positions, 0)

        # Test completely wrong guess
        guess = [4, 3, 2, 1]
        right_positions, wrong_positions = check_code(guess, code)
        self.assertEqual(right_positions, 0)
        self.assertEqual(wrong_positions, 4)

        # Test partially correct guess
        guess = [1, 2, 4, 3]
        right_positions, wrong_positions = check_code(guess, code)
        self.assertEqual(right_positions, 2)
        self.assertEqual(wrong_positions, 2)

        # Test guess with no correct positions
        guess = [5, 5, 5, 5]
        right_positions, wrong_positions = check_code(guess, code)
        self.assertEqual(right_positions, 0)
        self.assertEqual(wrong_positions, 0)

        # Test raise error for wrong length guess
        guess = [1, 2, 3]
        with self.assertRaises(ValueError):
            check_code(guess, code)

    def test_play_turn(self):
        game = MasterMind(n_colors=6, len_code=4, n_rounds=10)
        game.code = [1, 2, 3, 4]

        # Test correct guess
        guess = [1, 2, 3, 4]
        game._play_turn(guess)
        self.assertEqual(game.rounds[0]['guess'], guess)
        self.assertEqual(game.rounds[0]['right_positions'], 4)
        self.assertEqual(game.rounds[0]['wrong_positions'], 0)

        # Test completely wrong guess
        guess = [4, 3, 2, 1]
        game._play_turn(guess)
        self.assertEqual(game.rounds[1]['guess'], guess)
        self.assertEqual(game.rounds[1]['right_positions'], 0)
        self.assertEqual(game.rounds[1]['wrong_positions'], 4)

        # Test partially correct guess
        guess = [1, 2, 4, 3]
        game._play_turn(guess)
        self.assertEqual(game.rounds[2]['guess'], guess)
        self.assertEqual(game.rounds[2]['right_positions'], 2)
        self.assertEqual(game.rounds[2]['wrong_positions'], 2)

        # Test guess with no correct positions
        guess = [5, 5, 5, 5]
        game._play_turn(guess)
        self.assertEqual(game.rounds[3]['guess'], guess)
        self.assertEqual(game.rounds[3]['right_positions'], 0)
        self.assertEqual(game.rounds[3]['wrong_positions'], 0)

        # Test raise error for wrong length guess
        guess = [1, 2, 3]
        with self.assertRaises(ValueError):
            game._play_turn(guess)

        # Test raise error for out of range colors
        guess = [1, 2, 3, 6]
        with self.assertRaises(ValueError):
            game._play_turn(guess)

        self.assertEqual(len(game.rounds), 4)

    def test_call(self):
        game = MasterMind(n_colors=6, len_code=4, n_rounds=3)
        game.code = [1, 2, 3, 4]

        # Test correct guess
        guess = [1, 2, 3, 5]
        rounds = game(guess)
        self.assertEqual(rounds[0]['guess'], guess)
        self.assertEqual(rounds[0]['right_positions'], 3)
        self.assertEqual(rounds[0]['wrong_positions'], 0)

        # Test completely wrong guess
        guess = [4, 3, 2, 1]
        rounds = game(guess)
        self.assertEqual(rounds[1]['guess'], guess)
        self.assertEqual(rounds[1]['right_positions'], 0)
        self.assertEqual(rounds[1]['wrong_positions'], 4)

        # Test partially correct guess
        guess = [1, 2, 4, 3]
        rounds = game(guess)
        self.assertEqual(rounds[2]['guess'], guess)
        self.assertEqual(rounds[2]['right_positions'], 2)
        self.assertEqual(rounds[2]['wrong_positions'], 2)

        # Test exceeding number of rounds
        guess = [5, 5, 5, 5]
        rounds = game(guess)
        self.assertEqual(len(rounds), 3)
        self.assertNotIn(3, rounds)

        # Test game over
        guess = [1, 2, 3, 4]
        rounds = game(guess)
        self.assertEqual(len(rounds), 3)
        self.assertNotIn(4, rounds)

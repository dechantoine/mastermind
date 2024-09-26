from loguru import logger
import numpy as np


class MasterMind:
    def __init__(self,
                 n_colors: int = 8,
                 len_code: int = 5,
                 n_rounds: int = 12,
                 code: list[int] = None) -> None:
        """
        Initialize the game of MasterMind.

        Args:
            n_colors (int): number of colors in the game
            len_code (int): length of the code
            n_rounds (int): number of rounds
            code (list[int]): code to guess (if None, a random code is generated)
        """
        self.n_colors = n_colors
        self.len_code = len_code
        self.n_rounds = n_rounds

        self.game_over = False

        self.rounds = {}

        if code is not None:
            if len(code) != len_code:
                raise ValueError(f"Code must be of length {len_code}")
            if not all(0 <= color < n_colors for color in code):
                raise ValueError(f"Colors must be in the range 0 to {n_colors -1}")
            self.code = code

        else:
            self._generate_code()

    def _generate_code(self) -> None:
        """Generate a random code for the game."""
        self.code = np.random.randint(0, self.n_colors, self.len_code)

    def check_code(self, guess: list[int]) -> tuple[int, int]:
        """
        Check the guess against the code.

        Args:
            guess (list[int]): the guess

        Returns:
            tuple: number of right positions, number of wrong positions
        """
        if len(guess) != self.len_code:
            raise ValueError(f"Guess must be of length {self.len_code}")

        if not all(0 <= color < self.n_colors for color in guess):
            raise ValueError(f"Colors must be in the range 0 to {self.n_colors -1}")

        remaining_code = [c for i, c in enumerate(self.code)
                          if guess[i] != c]
        remaining_guess = [c for i, c in enumerate(guess)
                           if self.code[i] != c]

        right_positions = self.len_code - len(remaining_code)
        wrong_positions = 0

        while remaining_guess:
            c = remaining_guess.pop()
            if c in remaining_code:
                remaining_code.remove(c)
                wrong_positions += 1

        return right_positions, wrong_positions

    def _play_turn(self, guess: list[int]):
        """
        Play a turn of the game.

        Args:
            guess (list[int]): the guess

        Return:
            dict: the results of the turns so far
        """
        right_positions, wrong_positions = self.check_code(guess)
        self.rounds[len(self.rounds)] = {"guess": guess,
                                         "right_positions": right_positions,
                                         "wrong_positions": wrong_positions}

        if right_positions == self.len_code:
            logger.info("Code guessed!")
            self.game_over = True

        return self.rounds

    def __call__(self, guess: list[int]):
        if len(self.rounds) >= self.n_rounds or self.game_over:
            logger.warning("Game over.")
            self.game_over = True
            return self.rounds

        return self._play_turn(guess)

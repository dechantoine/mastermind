import json
from typing import Union
import os

from loguru import logger
import numpy as np

emojis = json.load(open(os.path.dirname(__file__) + "/emojis.json", "r"))


def get_emojis(n_colors: int = 8) -> str:
    """Get the emojis.

    Args:
        n_colors (int): number of colors

    Returns:
        str: the emojis for playing with this number of colors
    """
    return "".join(emoji for emoji in list(emojis.values())[:n_colors])


def code_to_emoji(code: list[int]) -> str:
    """Convert a code to emojis.

    Args:
        code (list[int]): the code

    Returns:
        str: the emojis representing the code
    """
    return "".join(emojis[str(color)] for color in code)


def emojis_to_code(emoji_str: str) -> list[int]:
    """Convert emojis to a code.

    Args:
        emoji_str (str): the emojis representing the code

    Returns:
        list: the code
    """
    return [list(emojis.values()).index(emoji) for emoji in list(emoji_str)]


def generate_code(n_colors: int = 8, len_code: int = 5) -> list[int]:
    """Generate a random code by sampling len_code from n_colors.

    Args:
        n_colors (int): number of colors
        len_code (int): length of the code

    Returns:
        list: the code
    """
    return np.random.randint(low=0,
                             high=n_colors,
                             size=len_code).tolist()


def check_code(guess: list[int], code: list[int]) -> tuple[int, int]:
    """
    Check the guess against the code.

    Args:
        guess (list[int]): the guess
        code (list[int]): the code

    Returns:
        tuple: number of right positions, number of wrong positions
    """
    if len(guess) != len(code):
        raise ValueError(f"Guess and code must be of the same length")

    remaining_code = [c for i, c in enumerate(code)
                      if guess[i] != c]
    remaining_guess = [c for i, c in enumerate(guess)
                       if code[i] != c]

    right_positions = len(code) - len(remaining_code)
    wrong_positions = 0

    while remaining_guess:
        c = remaining_guess.pop()
        if c in remaining_code:
            remaining_code.remove(c)
            wrong_positions += 1

    return right_positions, wrong_positions


class MasterMind:
    def __init__(self,
                 n_colors: int = 8,
                 len_code: int = 5,
                 n_rounds: int = 12,
                 code: Union[list[int], str] = None,
                 use_emojis: bool = False) -> None:
        """
        Initialize the game of MasterMind.

        Args:
            n_colors (int): number of colors in the game
            len_code (int): length of the code
            n_rounds (int): number of rounds
            code (Union[list[int], str]): code to guess (if None, a random code is generated)
            use_emojis (bool): whether to use emojis for colors
        """
        self.n_colors = n_colors
        self.len_code = len_code
        self.n_rounds = n_rounds
        self.use_emojis = use_emojis

        self.game_over = False
        self.win = None

        self.rounds = {}

        if code is not None:
            if isinstance(code, str):
                code = emojis_to_code(code)

            if len(code) != len_code:
                raise ValueError(f"Code must be of length {len_code}")
            if not all(0 <= color < n_colors for color in code):
                raise ValueError(f"Colors must be in the range 0 to {n_colors - 1}")

            self.code = code

        else:
            self.code = generate_code(n_colors=n_colors, len_code=len_code)

    def _play_turn(self, guess: list[int]):
        """
        Play a turn of the game.

        Args:
            guess (list[int]): the guess
        """
        if not all(0 <= color < self.n_colors for color in guess):
            raise ValueError(f"Colors must be in the range 0 to {self.n_colors - 1}")

        right_positions, wrong_positions = check_code(guess=guess, code=self.code)

        self.rounds[len(self.rounds)] = {"guess": guess,
                                         "right_positions": right_positions,
                                         "wrong_positions": wrong_positions}

        if right_positions == self.len_code:
            logger.info("Code guessed!")
            self.game_over = True
            self.win = True
            return self.rounds

        if len(self.rounds) == self.n_rounds:
            logger.info("Game over: out of rounds.")
            self.game_over = True
            self.win = False

    def __call__(self, guess: Union[list[int], str]) -> dict:
        if self.game_over:
            logger.warning("Game over.")
            return self.rounds

        if isinstance(guess, str):
            guess = emojis_to_code(guess)

        self._play_turn(guess)
        rounds = {k: v.copy() for k, v in self.rounds.items()}

        if not self.use_emojis:
            return rounds

        else:
            for _, round_ in rounds.items():
                round_["guess"] = code_to_emoji(round_["guess"])
            return rounds

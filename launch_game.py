"""
This is the entry point to your game.

Launch the game by running `python3 launch_game.py`
"""

from game_engine import Engine
from gui import GUI
from player import Player

game = Engine('examples/game_state_good.txt', Player, GUI)
#game.import_state('examples/game_state_good.txt')
game.run_game()

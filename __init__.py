from game.core.core import Core
from game.ui_manager.screens import Screen_Game

if __name__ == '__main__':
    Core(fps=True).start(Screen_Game())

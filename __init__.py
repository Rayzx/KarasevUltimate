import json

from game.core.core import Core
from game.ui_manager.screens import Screen_Game

if __name__ == '__main__':
    output_file = open('resources/settings.json').read()
    Core(json.loads(output_file)).start(Screen_Game())

import json

from game.core.core import Core
from game.ui_manager.screens import Screen_Game, Screen_Menu

if __name__ == '__main__':
    output_file = open('resources/settings.json', 'r')
    d = json.loads(output_file.read())
    output_file.close()
    Core(d).start(Screen_Menu())
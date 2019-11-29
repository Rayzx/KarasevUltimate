import json

from game.core.core import Core
from game.ui_manager.screens import ScreenMenu

if __name__ == '__main__':
    d = None
    try:
        output_file = open('resources/settings.json', 'r')
        d = json.loads(output_file.read())
        output_file.close()
    except FileNotFoundError as e:
        d = {"width": 800, "height": 600, "fps": True}

        j = json.dumps(d)

        f = open("resources/settings.json", "w")
        f.write(j)
        f.close()

    finally:
        Core(d).start(ScreenMenu())

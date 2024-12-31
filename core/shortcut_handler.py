from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

class ShortcutHandler:
    def __init__(self, parent, shortcut_map):
        """
        Initializes the ShortcutHandler.

        Params: 
            parent: The parent widget (e.g., MainWindow) to attach shortcuts to.
            shortcut_map: A dictionary mapping key sequences to actions.
        """
        self.parent = parent
        self.shortcut_map = shortcut_map
        self.shortcuts = []
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """
        Sets up the shortcuts based on the provided shortcut map.
        """
        for key_sequence, action in self.shortcut_map.items():
            shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
            shortcut.activated.connect(action)
            self.shortcuts.append(shortcut)

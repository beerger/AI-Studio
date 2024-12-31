from pathlib import Path
from PyQt5 import QtGui
import os
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = PROJECT_ROOT / "resources" / "icons"

def get_absolute_path(directory, filename):
    """
    Get the absolute path of a file relative to the project root.
    """
    return str(PROJECT_ROOT / directory / filename).replace("\\", "/")

def load_json(directory, filename):
    """
    Load a JSON file from the specified directory.
    """
    with open(get_absolute_path(directory, filename), "r") as json_file:
        return json.load(json_file)
    
def get_value_from_json(json_data, path):
    for key in path:
        json_data = json_data[key]
    return json_data

def create_icon(icon_png):
    """
    Creates a QIcon from the given path parts.
    """
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(os.path.join(ICON_DIR, icon_png)), QtGui.QIcon.Selected, QtGui.QIcon.On)
    return icon
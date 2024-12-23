from PyQt5 import QtWidgets, QtCore
from functools import partial
import json

class ComponentLayoutWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.component_params = self.load_component_params()

        # Main layout for this widget
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create a QTreeWidget
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)  # Hide the header
        layout.addWidget(self.tree_widget)

        # Populate the tree with the component parameters
        self.populate_tree(self.tree_widget, self.component_params)

        # Expand all items by default
        self.tree_widget.expandAll()

    def populate_tree(self, parent_widget, data):
        """Populate the QTreeWidget, stopping when a 'parameters' field is encountered."""
        for key, value in data.items():
            # Add a tree item for the current key
            tree_item = QtWidgets.QTreeWidgetItem(parent_widget)
            formatted_name =  value.get('formatted_name')
            if formatted_name:
                tree_item.setText(0, formatted_name)
            else:
                tree_item.setText(0, key.capitalize())

            # Check if the current value is a dictionary
            if isinstance(value, dict):
                # Stop if the dictionary contains a 'parameters' field
                print(value)
                print(key)
                if "parameters" in value:
                    continue
                # Otherwise, recurse into the dictionary
                self.populate_tree(tree_item, value)
        
    def load_component_params(self):
        """
        Loads the component parameters from a JSON file.
        """
        # FIXME: Change the path to the JSON file relative to your project
        with open("D:/OneDrive - Uppsala universitet/General/AI-Studio/models/component_params.json", "r") as json_file:
            return json.load(json_file)



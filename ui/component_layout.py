from PyQt5 import QtWidgets, QtCore
from functools import partial
from utils.file_helper import load_json, get_value_from_json
from ui.add_component_popup import AddComponentPopup

class ComponentLayoutWidget(QtWidgets.QWidget):
    # Define the signal at the class level
    def __init__(self, signal_manager, parent=None):
        super().__init__(parent)
        self.signal_manager = signal_manager
        self.components_json = load_json('models', 'component_params.json')

        # Main layout for this widget
        layout = QtWidgets.QVBoxLayout(self)
        
        # Create a QTreeWidget
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)  # Hide the header
        layout.addWidget(self.tree_widget)

        # Populate the tree with the component parameters
        self.populate_tree(self.tree_widget, self.components_json)
        
        self.tree_widget.itemClicked.connect(self.onItemClicked)
        # Expand all items by default
        self.tree_widget.expandAll()
        
    def populate_tree(self, parent_widget, data):
        """Populate the QTreeWidget and store raw keys for JSON traversal."""
        for key, value in data.items():
            # Add a tree item for the current key
            tree_item = QtWidgets.QTreeWidgetItem(parent_widget)

            # Display the formatted name (if available) or the capitalized key
            formatted_name = value.get('formatted_name') if isinstance(value, dict) else None
            tree_item.setText(0, formatted_name if formatted_name else key.capitalize())

            # Store the raw key as custom data
            tree_item.setData(0, QtCore.Qt.UserRole, key)

            # Check if it's an end node
            if isinstance(value, dict) and "parameters" in value:
                tree_item.setFlags(tree_item.flags() | QtCore.Qt.ItemIsSelectable)  # Make selectable
                continue
            else:
                tree_item.setFlags(tree_item.flags() & ~QtCore.Qt.ItemIsSelectable)  # Disable selection

            # Recurse into the dictionary
            if isinstance(value, dict):
                self.populate_tree(tree_item, value)
    
    def get_full_json_path(self, item):
        """Reconstruct the full path in the JSON using stored raw keys."""
        path = []
        while item is not None:
            raw_key = item.data(0, QtCore.Qt.UserRole)  # Retrieve the stored raw key
            path.insert(0, raw_key)  # Insert at the beginning
            item = item.parent()  # Move to the parent item
        return path
    
    def close_existing_popup(self):
        """Close the existing popup if it's open."""
        if hasattr(self, "popup") and self.popup:
            self.popup.close()
            self.popup = None
    
    def on_popup_closed(self, obj):
        """Reset the popup reference when the popup is closed."""
        self.popup = None
    
    def onItemClicked(self, item, column):
        """
        Handle the itemClicked signal for the QTreeWidget.
        """
        # Do nothing if the item is not selectable
        if not (item.flags() & QtCore.Qt.ItemIsSelectable):
            return
        
        # Close the existing popup if it's open
        self.close_existing_popup()

        component_dict = get_value_from_json(self.components_json, self.get_full_json_path(item))
        raw_name = item.data(0, QtCore.Qt.UserRole) 
        
        self.popup = AddComponentPopup(component_dict, self.signal_manager, parent=self)
        
        # Disconnect existing connections to avoid duplicates
        # Since the SignalOwner class owns the signal
        try:
            self.signal_manager.component_added_signal.disconnect()
        except TypeError:
            # If no connections exist, it's safe to ignore this
            pass
        
        # Connect the custom signal to the slot method
        self.signal_manager.component_added_signal.connect(partial(self.handle_component_added, raw_name))
        self.popup.show()

        # Ensure the popup reference is reset when closed
        self.popup.destroyed.connect(self.on_popup_closed)
        
    def handle_component_added(self, raw_name, args):
        """
        Slot to handle the component_added_signal signal from the popup.
        """
        component_data = {'name': raw_name, 'args': args}
        # Emit the signal to propagate data to the MainWindow
        self.signal_manager.components_updated_signal.emit(component_data)
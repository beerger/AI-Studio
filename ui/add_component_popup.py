from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from utils.file_helper import load_json
from core.signal_manager import SignalManager

class AddComponentPopup(QtWidgets.QWidget):
    def __init__(self, component_dict, signal_manager, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window) # Make it a top-level window
        self.setWindowTitle("New Component")
        self.component_dict = component_dict
        self.signal_manager = signal_manager
        self.input_widgets = []
        self.args = {}

        # Load component parameters from JSON
        self.component_params = load_json('models', 'component_params.json')    

        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        vertical_layout = QtWidgets.QVBoxLayout(self)

        self.description_label = QtWidgets.QLabel()
        self.description_label.setWordWrap(True)  # Allow wrapping for long text
        self.description_label.setText("Click on a parameter label to see its description.")
        vertical_layout.addWidget(self.description_label)

        # Create grid layout for parameters
        grid_layout = QtWidgets.QGridLayout()
        for i, param in enumerate(self.component_dict['parameters']):
            label = QtWidgets.QLabel()
            param_name = param['name']
            required = param['required']
            label_text = ' '.join(map(str.capitalize, param_name.split('_')))
            
            if not required:
                label.setText(f"{label_text} (optional)")
            else:
                label.setText(label_text)
                
            myFont=QtGui.QFont()
            myFont.setBold(True)
            label.setFont(myFont)
            label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            label.setToolTip(param['description'])
            label.mousePressEvent = partial(self.update_description, param['description'])
            grid_layout.addWidget(label, i, 0)

            # If choices or bool, use dropdown
            choices = param.get('choices')
            type_ = param['type']
            input_widget = None
            if choices or "bool" in type_:
                input_widget = QtWidgets.QComboBox()
                input_widget.addItems(choices if choices else ['True', 'False'])
                input_widget.setCurrentText(str(param['default']).capitalize())
            else: 
                input_widget = QtWidgets.QLineEdit()
                if not required:
                    input_widget.setPlaceholderText(str(param['default']))

            input_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            input_widget.param_name = param_name  # Associate with the parameter name
            
            grid_layout.addWidget(input_widget, i, 1)
            self.input_widgets.append(input_widget)

        vertical_layout.addLayout(grid_layout)

        # Add documentation label
        documentation_label = QtWidgets.QLabel()
        documentation_label.setText(f"Click here for full documentation")
        documentation_label.setOpenExternalLinks(True)
        documentation_label.mousePressEvent = partial(self.open_documenation, self.component_dict['documentation'])
        
        vertical_layout.addWidget(documentation_label)
        
        # Add button
        button = QtWidgets.QPushButton("Add Component")
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.clicked.connect(self.clicked_add_component)
        vertical_layout.addWidget(button)
        
    def get_args(self):
        return self.args

    def open_documenation(self, url, event):
        """
        Opens the documentation link in the browser when clicked.
        """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))    
        
    def update_description(self, param_desc, event):
        """
        Updates the description label when a parameter's textbox is focused.
        """
        self.description_label.setText(param_desc)

    def clicked_add_component(self):
        """
        Collects and validates user input.
        """
        invalid_params = []
        for i, widget in enumerate(self.input_widgets):
            if isinstance(widget, QtWidgets.QComboBox):
                value = widget.currentText()
            else:
                value = widget.text().strip() or widget.placeholderText()
            
            param_info = self.component_dict['parameters'][i]
            parsed_value = self.parse_value(value, param_info)
            if parsed_value is None and "null" not in param_info['type']:
                invalid_params.append(widget.param_name)
            else:
                self.args[widget.param_name] = parsed_value
        if invalid_params:
            QtWidgets.QMessageBox.warning(self, "Invalid Parameters", f"Invalid parameters: {', '.join(invalid_params)}")
            self.args = {}
        else:
            # Emit the signal with the collected arguments
            self.signal_manager.component_added_signal.emit(self.args)
            self.close()

    def parse_value(self, value, param_info):
        """
        Parses and validates the user input.
        """
        valid_types = param_info['type']
        choices = param_info.get('choices')
        try:
            if value == "None" and "null" in valid_types:
                return None
            # handle negative numbers
            if value.startswith('-'):
                value = value[1:]
            if "int" in valid_types and value.isdigit():
                return int(value)
            if "float" in valid_types:
                return float(value)
            if "str" in valid_types:
                return value
            if "bool" in valid_types:
                return value.lower() == 'true'
            if "tuple" in valid_types:
                return tuple(map(int, value.strip("()").split(',')))
            # No need to check for bool since it's a dropdown
            # No need to check for choices since it's a dropdown
            return None
        except (ValueError, TypeError):
            return None


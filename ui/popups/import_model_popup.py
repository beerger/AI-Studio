from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QLabel, QFileDialog, QMessageBox, QTextEdit, QHBoxLayout, QWidget, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
import torch
import constants.tooltips as tt
from models.pytorch_models import MODELS
import torchvision.models as models
import inspect
from core.components import WRAPPER_REGISTRY
from ui.popups.frameless_popup import FrameLessPopup
from PyQt5 import QtCore

class ImportModelPopup(FrameLessPopup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # Update the title in the custom title bar
        self.title_label.setText("Import Model")

        # Use the content layout provided by FrameLessPopup
        self.form_layout = QFormLayout()

        # Model path and type selection
        self.model_path = QLineEdit()
        self.model_path_label = QLabel("Model Path")
        self.model_type = QComboBox()
        self.model_type.addItems(["PyTorch", "ONNX"])
        self.model_type_label = QLabel("Model Type")

        # Add model type to the form layout
        self.form_layout.addRow(self.model_type_label, self.model_type)

        # Setup combo boxes
        self.setup_combo_boxes()

        # Add model path to the form layout
        self.form_layout.addRow(self.model_path_label, self.model_path)

        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)
        self.form_layout.addRow(self.browse_button)

        # Add form layout to the content layout
        self.content_layout.addLayout(self.form_layout)

        # Add scroll area for additional options
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)

        self.container = QWidget()
        self.container_layout = QHBoxLayout(self.container)
        self.container.setLayout(self.container_layout)
        self.scroll_area.setWidget(self.container)

        self.content_layout.addWidget(self.scroll_area)

        # Import button
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.import_model)
        self.content_layout.addWidget(self.import_button)
    
    def import_model(self):
        model = models.__dict__[self.model_combo.currentText()](weights=self.weights_combo.currentText())
        self.wrappers = self.parse_model()
        self.showMaximized()
        self.render_network()
    
    def setup_combo_boxes(self):
        self.category_combo = QComboBox()
        self.architecture_combo = QComboBox()
        self.model_combo = QComboBox()
        self.weights_combo = QComboBox()

        self.form_layout.addRow("Category", self.category_combo)
        self.form_layout.addRow("Architecture", self.architecture_combo)
        self.form_layout.addRow("Model", self.model_combo)
        self.form_layout.addRow("Weights", self.weights_combo)

        for category in MODELS.keys():
            self.category_combo.addItem(category)

        self.update_architectures()
        
        self.category_combo.currentIndexChanged.connect(self.update_architectures)
        self.architecture_combo.currentIndexChanged.connect(self.update_models)
        self.model_combo.currentIndexChanged.connect(self.update_weights)


    def update_architectures(self):
        # Block signals to prevent the currentIndexChanged signal from being emitted
        self.architecture_combo.blockSignals(True)
        self.model_combo.blockSignals(True)
        self.weights_combo.blockSignals(True)
        
        self.architecture_combo.clear()
        self.model_combo.clear()
        self.weights_combo.clear()
        
        category = self.category_combo.currentText()
        for architecture in MODELS[category].keys():
            self.architecture_combo.addItem(architecture)
        self.architecture_combo.blockSignals(False)
        self.update_models() # Trigger the update of the models
    
    def update_models(self):
        self.model_combo.blockSignals(True)
        self.weights_combo.blockSignals(True)
        self.model_combo.clear()
        self.weights_combo.clear()
        category = self.category_combo.currentText()
        architecture = self.architecture_combo.currentText()
        for model in MODELS[category][architecture]["models"].keys():
            self.model_combo.addItem(model)
        self.model_combo.blockSignals(False)
        self.update_weights() # Trigger the update of the weights

    def update_weights(self):
        self.weights_combo.blockSignals(True)
        self.weights_combo.clear()
        category = self.category_combo.currentText()
        architecture = self.architecture_combo.currentText()
        model = self.model_combo.currentText()
        for weights in MODELS[category][architecture]["models"][model]["weights"]:
            self.weights_combo.addItem(weights)
        self.weights_combo.blockSignals(False)
        
    def browse(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Model files (*.pt *.onnx)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.model_path.setText(file_path)
    
    def parse_model(self):
        model = models.__dict__[self.model_combo.currentText()](weights=self.weights_combo.currentText())
        layers = []
        layers = self.populate_model(model, layers)

        wrappers = []
        for layer in layers:
            raw_name = layer.__class__.__name__
            wrapper_class = WRAPPER_REGISTRY.get(raw_name)
            if not wrapper_class:
                print("skip")
                continue
            params = self.extract_params(layer)
            component = wrapper_class(raw_name, params)
            wrappers.append(component)
        return wrappers
        
            
    def populate_model(self, model, layers):
        for layer in list(model.children()):
            if len(list(layer.children())) > 0:
                self.populate_model(layer, layers)
            else:
                layers.append(layer)
        return layers
    
    def extract_params(self, layer):
        params = {}
        try:
            # Get the valid arguments for the layer's __init__ method
            signature = inspect.signature(layer.__class__.__init__)
            valid_args = signature.parameters.keys()

            for arg in valid_args:
                if hasattr(layer, arg):
                    value = getattr(layer, arg)
                    # Special handling for the 'bias' argument
                    if arg == "bias" and isinstance(value, torch.Tensor):
                        params[arg] = value is not None  # Convert tensor to boolean
                    else:
                        params[arg] = value
        except Exception as e:
            print(f"Failed to extract parameters from {layer.__class__.__name__}: {e}")
        return params
    
    def render_network(self):
        # Clear the layout in the container
        self.clear_layout(self.container_layout)

        for component in self.wrappers:
            widget = component.get_widget()
            scaling_factor = widget.scaling_factor if hasattr(widget, 'scaling_factor') else 1
            component_height = max(50, int(self.height() * 0.3 * scaling_factor))
            component_width = max(50, int(self.width() * 0.1 * scaling_factor))
            widget.setFixedSize(component_width, component_height)

            current_stylesheet = widget.styleSheet()
            font_stylesheet = "font-size: 32px;"
            widget.setStyleSheet(current_stylesheet + font_stylesheet)
            self.container_layout.addWidget(widget)

            self.add_line()

        # Add a spacer for alignment
        self.container_layout.addStretch()

        
    def add_line(self):
        line_height = max(1, int((self.height() * 0.3) // 150))  # Adjust the thickness of the line #TODO: Make dynamic
        line_width = int((self.width() * 0.1) // 3)  # One-third of the component width

        # Create a custom line using QLabel or QWidget
        line = QWidget()
        line.setAccessibleName("line")
        line.setFixedHeight(line_height)
        line.setFixedWidth(line_width)
        line.setStyleSheet("background-color: black;")  # Set the color and thickness
        self.container_layout.addWidget(line)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
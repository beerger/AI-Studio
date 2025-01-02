from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QCheckBox, QPushButton, QLabel, QFileDialog, QMessageBox, QTextEdit, QHBoxLayout
)
import torch
import constants.tooltips as tt

class ONNXParametersPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ONNX export") 
        self.sizes = {
                'torch.float32': 4,
                'torch.float16': 2,
                'torch.float64': 8,
                'torch.int32': 4,
                'torch.int64': 8,
                'torch.bool': 1,
                'torch.complex64': 8,
                'torch.complex128': 16,
                'torch.int8': 1,
                'torch.uint8': 1,
                'torch.bfloat16': 2
            }
        
        # Main layout
        layout = QVBoxLayout(self)

        # Form layout for input dimensions
        self.form_layout = QFormLayout()
        self.batch_size_input = QLineEdit("1")
        self.channels_input = QLineEdit("3")
        self.height_input = QLineEdit("224")
        self.width_input = QLineEdit("224")
        
        # Help text
        help_label = QLabel(
            "Specify dimensions for the input tensor. \nHover the mouse over each field for more information."
        )
        help_label.setStyleSheet("color: gray; font-size: 14px;")
        layout.addWidget(help_label)

        self.form_layout.addRow("Batch Size:", self.batch_size_input)
        self.form_layout.addRow("Channels:", self.channels_input)
        self.form_layout.addRow("Height:", self.height_input)
        self.form_layout.addRow("Width:", self.width_input)

        # Checkbox to enable dynamic shapes
        self.dynamic_shapes_checkbox = QCheckBox("Enable Dynamic Shapes")
        self.dynamic_shapes_checkbox.stateChanged.connect(self.toggle_dynamic_shapes)
        self.form_layout.addRow(self.dynamic_shapes_checkbox)

        # Data type selector
        self.data_type_selector = QComboBox()
        self.data_type_selector.addItems(self.sizes.keys())
        self.form_layout.addRow("Data Type:", self.data_type_selector)

        self.tensor_value_selector = QComboBox()
        self.tensor_value_selector.addItems([
                    'Random',
                    'Zeros',
                    'Ones',
                    'Identity',
                    'Custom'
        ])
        
        self.tensor_value_selector.currentIndexChanged.connect(self.toggle_tensor_value)
        self.form_layout.addRow("Tensor Value:", self.tensor_value_selector)
        
        # Save path
        self.save_path_input = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.select_save_path)
        self.form_layout.addRow("Save Path:", self.save_path_input)
        self.form_layout.addRow("", self.browse_button)  # Aligns the button with the input field

        # Buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.validate_values)
        self.cancel_button.clicked.connect(self.reject)

        layout.addLayout(self.form_layout)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        
        self.set_tooltips()
    
    def set_tooltips(self):

        # Example assignments
        self.batch_size_input.setToolTip(tt.BATCH_SIZE_TOOLTIP)
        self.channels_input.setToolTip(tt.CHANNELS_TOOLTIP)
        self.height_input.setToolTip(tt.HEIGHT_TOOLTIP)
        self.width_input.setToolTip(tt.WIDTH_TOOLTIP)
        self.dynamic_shapes_checkbox.setToolTip(tt.DYNAMIC_SHAPES_TOOLTIP)
        self.data_type_selector.setToolTip(tt.DATA_TYPE_TOOLTIP)
        self.tensor_value_selector.setToolTip(tt.TENSOR_VALUE_TOOLTIP)
        self.save_path_input.setToolTip(tt.SAVE_PATH_TOOLTIP)
        self.browse_button.setToolTip(tt.BROWSE_BUTTON_TOOLTIP)
        self.ok_button.setToolTip(tt.OK_BUTTON_TOOLTIP)
        self.cancel_button.setToolTip(tt.CANCEL_BUTTON_TOOLTIP)

    
    def toggle_tensor_value(self):
        if self.tensor_value_selector.currentText() == 'Custom':
            try:             
                batch_size = int(self.batch_size_input.text())
                channels = int(self.channels_input.text())
                height = int(self.height_input.text())
                width = int(self.width_input.text())
                if any(dim < 1 for dim in [batch_size, channels, height, width]):
                    raise ValueError("All dimensions must be 1 or greater.")
            except ValueError as e:
                QMessageBox.warning(self, "Invalid", "Please enter valid dimensions for the tensor before specifying values.")
                return
            popup = TensorValuePopup((batch_size, channels, height, width))
            if popup.exec_() == QDialog.Accepted:
                tensor_values = popup.get_tensor_values()
                print(tensor_values)
               
    def toggle_dynamic_shapes(self) -> None:
        """
        Handle enabling/disabling dynamic shapes.
        """
        if self.dynamic_shapes_checkbox.isChecked():
            # Automatically lock channels, height, width to defaults and disable editing
            self.batch_size_input.setText("1")
            self.channels_input.setText("3")
            self.height_input.setText("224")
            self.width_input.setText("224")
            self.batch_size_input.setDisabled(True)
            self.channels_input.setDisabled(True)
            self.height_input.setDisabled(True)
            self.width_input.setDisabled(True)
        else:
            # Re-enable editing for all fields
            self.batch_size_input.setDisabled(False)
            self.channels_input.setDisabled(False)
            self.height_input.setDisabled(False)
            self.width_input.setDisabled(False)

    def select_save_path(self) -> None:
        # Open a file dialog to select the save path
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save ONNX File", "", "ONNX Files (*.onnx);;All Files (*)"
        )
        if save_path:
            self.save_path_input.setText(save_path)

    def validate_values(self) -> None:
        
        try:
            batch_size = int(self.batch_size_input.text())
            channels = int(self.channels_input.text())
            height = int(self.height_input.text())
            width = int(self.width_input.text())
            data_type = self.data_type_selector.currentText()
            if data_type == "--- Advanced Options ---":
                raise ValueError("Please select a valid data type.")
            save_path = self.save_path_input.text()

            tensor_size = batch_size * channels * height * width * self.sizes[data_type.split(" ")[0]]
            
            if any(dim < 1 for dim in [batch_size, channels, height, width]):
                raise ValueError("All dimensions must be 1 or greater.")
            if tensor_size > 2 * 10**9:
                raise ValueError("Tensor size exceeds 2GB limit.\nCalculated size: {} {}".format(tensor_size // 10**12 if tensor_size > 10**12 else tensor_size // 10**9, "TB" if tensor_size > 10**12 else "GB"))   
            if not save_path:
                raise ValueError("Save path must be specified.")

            # trigger self.accept
            self.accept()
        except ValueError as e:
            
            QMessageBox.warning(self, "Invalid", f"{e}")            
            
    # Only safe to call after validate_values
    def get_values(self) -> dict:
        return {
            "batch_size": int(self.batch_size_input.text()),
            "channels": int(self.channels_input.text()),
            "height": int(self.height_input.text()),
            "width": int(self.width_input.text()),
            "data_type": self.data_type_selector.currentText().split(" ")[0].replace("torch.", ""),
            "tensor_value": self.tensor_value_selector.currentText(),
            "save_path": self.save_path_input.text(),
            "dynamic_shapes": self.dynamic_shapes_checkbox.isChecked()
        }

class ONNXErrorPopup(QDialog):
    RETRY = 1
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Export failed") 
        self.layout = QVBoxLayout()
        
        self.main_text = QLabel("Failed to export the model to ONNX. Press 'See more' for details. Press 'Retry' to try again.")
        self.main_text.setWordWrap(True)
        self.layout.addWidget(self.main_text)
        
        self.detailed_text = QTextEdit(message)
        self.detailed_text.setReadOnly(True)
        self.detailed_text.hide()
        self.layout.addWidget(self.detailed_text)
        
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)
        
        self.see_more_button = QPushButton("See More")
        self.see_more_button.clicked.connect(self.see_more)
        
        self.retry_button = QPushButton("Retry")
        self.retry_button.clicked.connect(self.retry)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.see_more_button)
        button_layout.addWidget(self.retry_button)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)

    def see_more(self):
        if self.detailed_text.isVisible():
            self.detailed_text.hide()
            self.see_more_button.setText("See More")
        else:
            self.detailed_text.show()
            self.see_more_button.setText("Hide Details")
            
    
    def retry(self):
        return self.done(self.RETRY)
    
class TensorValuePopup(QDialog):
    def __init__(self, shape, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Specify Tensor Values")
        self.shape = shape

        self.layout = QVBoxLayout(self)
        self.label = QLabel(f"Enter values for tensor of shape {shape}:")
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_tensor_values(self):
        text = self.text_edit.toPlainText()
        values = [float(x) for x in text.split(",")]
        try:
            tensor = torch.tensor(values).reshape(self.shape)
            return tensor
        except RuntimeError as e:
            QMessageBox.warning(self, "Invalid", f"Error creating tensor: {e}")
            return None
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from utils.session_state import SessionState
from core.model_manager import ModelManager
from core.signal_manager import SignalManager
from core.code_generator import CodeGenerator
from core.onnx_exporter import ONNXExporter
from ui.popups.onnx_popup import ONNXParametersPopup, ONNXErrorPopup
from ui.popups.file_popup import get_output_popup
from ui.popups.import_model_popup import ImportModelPopup
from ui.popups.custom_messagebox import CustomMessageBox
from ui.popups.custom_progress_dialog import CustomProgressDialog
import torch
import os

class ToolsController:
    
    def __init__(self, signal_manager: SignalManager):
        self.model_manager = ModelManager()
        self.signal_manager = signal_manager
        self.setup_connections()

    def setup_connections(self) -> None:
        self.signal_manager.validate_network_signal.connect(self.validate_network)
        self.signal_manager.generate_summary_signal.connect(self.generate_summary)
        self.signal_manager.import_pretrained_signal.connect(self.import_pretrained)
        self.signal_manager.export_onnx_signal.connect(self.export_onnx)
        self.signal_manager.generate_code_signal.connect(self.generate_code)

    def validate_network(self) -> None:
        """
        Validates the network and displays any errors.
        """
        input_tensor = torch.randn(1, 3, 224, 224)
        try:
            self.model_manager.forward(input_tensor)
            CustomMessageBox.info(None, "Validation", "Network is valid")
        except Exception as e:
            CustomMessageBox.error(None, "Validation", f"Network is invalid: {e}")
    
    def generate_summary(self) -> None:
        """
        Generates a summary of the network.
        """
        print("Generating summary...")
    
    def import_pretrained(self) -> None:
        """
        Imports a pretrained model.
        """
        popup = ImportModelPopup()
        if popup.exec_() == QtWidgets.QDialog.Accepted:
            #values = popup.get_values()
            print(f"Importing model")
    
    def export_onnx(self) -> None:
        """
        Exports the network to ONNX format with progress bar and error handling.
        """
        popup = ONNXParametersPopup()
        if popup.exec_() == QtWidgets.QDialog.Accepted:
            values = popup.get_values()

            # Initialize exporter
            exporter = ONNXExporter("MyModel", values)

            # Create a progress dialog
            progress_dialog = CustomProgressDialog("Exporting model", "Test")#QtWidgets.QProgressDialog("Exporting model...", "Cancel", 0, 100)
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.setValue(0)

            # Connect exporter signals
            exporter.progress_signal.connect(progress_dialog.setValue)
            exporter.success_signal.connect(lambda: CustomMessageBox.information(None, "Export", "Model successfully exported to ONNX"))
            exporter.success_signal.connect(progress_dialog.close_safely)
            exporter.error_signal.connect(lambda msg: self.handle_onnx_error(msg, values))
            exporter.error_signal.connect(progress_dialog.close_safely)
            progress_dialog.canceled.connect(exporter.terminate)  # Allow canceling export

            # Start export in a separate thread
            exporter.start()

            # Show progress dialog
            progress_dialog.exec_()

    def handle_onnx_error(self, error_message: str, values: dict):
        """
        Handles errors during export and shows the error popup.
        """
        error_popup = ONNXErrorPopup(f"Error during ONNX export: {error_message}")
        if error_popup.exec_() == ONNXErrorPopup.RETRY:
            self.export_onnx()  # Reopen the parameter popup for retry
            
    def generate_code(self) -> None:
        """
        Generates code for the network.
        """
        output_dir = get_output_popup()
        if not output_dir:
            return
        code_generator = CodeGenerator(output_dir)
        code_generator.generate_all()
        reply = QtWidgets.QMessageBox.question(
            None, "Open", f"Code generation complete\nGenerated code can be found in {output_dir}\nOpen in VS Code?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        # open output directory in VS Code
        if reply == QtWidgets.QMessageBox.Yes:
            os.system(f'code "{output_dir}"')
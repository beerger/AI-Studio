from PyQt5 import QtWidgets
from utils.session_state import SessionState
from core.model_manager import ModelManager
from core.signal_manager import SignalManager
from core.code_generator import CodeGenerator
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
            QtWidgets.QMessageBox.information(None, "Validation", "Network is valid")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Validation", f"Network is invalid: {e}")
    
    def generate_summary(self) -> None:
        """
        Generates a summary of the network.
        """
        print("Generating summary...")
    
    def import_pretrained(self) -> None:
        """
        Imports a pretrained model.
        """
        print("Importing pretrained model...")
    
    def export_onnx(self) -> None:
        """
        Exports the network to ONNX format.
        """
        print("Exporting to ONNX...")
    
    def generate_code(self) -> None:
        """
        Generates code for the network.
        """
        output_dir = self.output_dir_popup()
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
    
    def output_dir_popup(self) -> str:
        """
        Opens a dialog to get the output directory.
        
        Return: 
            The selected directory or an empty string if canceled.
        """
        answer = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Output Directory", "")
        if answer == QtWidgets.QFileDialog.Rejected:
            return ""
        return answer
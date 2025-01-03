from PyQt5 import QtCore
import torch
import os
import sys
import tempfile
import importlib
from core.code_generator import CodeGenerator

class ONNXExporter(QtCore.QThread):
    progress_signal = QtCore.pyqtSignal(int)  # Signal to update progress bar
    success_signal = QtCore.pyqtSignal()  # Signal for successful export
    error_signal = QtCore.pyqtSignal(str)  # Signal for export errors

    def __init__(self, model_name: str, values: dict, parent=None):
        super().__init__(parent)
        self.model_name = model_name
        self.values = values
        self.temp_path = None

    def run(self):
        try:
            # Create a temporary file for the model code
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", dir=os.getcwd()) as tmp_file:
                self.temp_path = tmp_file.name
                print(f"Temporary file created at: {self.temp_path}")

            self.progress_signal.emit(10)  # Update progress

            # Generate model code dynamically
            code_generator = CodeGenerator(output_dir="", model_name=self.model_name)
            code_generator.generate_model_code(self.temp_path)
            self.progress_signal.emit(30)

            # Dynamically import the generated model
            module_name = os.path.splitext(os.path.basename(self.temp_path))[0]
            sys.path.append(os.getcwd())
            tmp_module = importlib.import_module(module_name)
            importlib.reload(tmp_module)
            torch_model = tmp_module.MyModel()
            self.progress_signal.emit(50)

            # Extract values
            batch_size = self.values['batch_size']
            channels = self.values['channels']
            height = self.values['height']
            width = self.values['width']
            save_path = self.values['save_path']
            dtype = self.values['data_type']
            is_dynamic = self.values['dynamic_shapes']

            # Create dummy input tensor
            input_tensor = torch.randn(
                (batch_size, channels, height, width),
                dtype=getattr(torch, dtype)
            )
            self.progress_signal.emit(70)

            # Export to ONNX
            export_options = torch.onnx.ExportOptions(dynamic_shapes=is_dynamic)
            onnx_program = torch.onnx.dynamo_export(
                torch_model,
                input_tensor,
                export_options=export_options
            )
            onnx_program.save(save_path)
            self.progress_signal.emit(100)

            # Notify success
            self.success_signal.emit()
            print(f"Model successfully exported to ONNX at: {save_path}")
        except Exception as e:
            self.progress_signal.emit(100)
            self.error_signal.emit(str(e))
        finally:
            # Ensure the temporary file is removed
            if self.temp_path and os.path.exists(self.temp_path):
                os.remove(self.temp_path)
                print(f"Temporary file removed: {self.temp_path}")
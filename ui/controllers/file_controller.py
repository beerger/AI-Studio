from PyQt5 import QtWidgets
from utils.session_state import SessionState
from core.model_manager import ModelManager
from core.signal_manager import SignalManager

class FileController:
    CONFIRMATION_TITLE = "Confirmation"
    NEW_NETWORK_MESSAGE = "Are you sure you want to start a new network?"
    CLOSE_MESSAGE = "Are you sure you want to close the application?"
    FILE_DIALOG_FILTER = "Pickle Files (*.pkl)"
    
    def __init__(self, signal_manager: SignalManager):
        self.model_manager = ModelManager()
        self.signal_manager = signal_manager
        self.setup_connections()

    def setup_connections(self) -> None:
        self.signal_manager.new_signal.connect(self.new_network)
        self.signal_manager.open_signal.connect(self.open_file)
        self.signal_manager.save_signal.connect(self.save)
        self.signal_manager.save_as_signal.connect(self.save_as)
        self.signal_manager.close_signal.connect(self.close_main_window)

    def show_confirmation_dialog(self, message: str) -> bool:
        """
        Displays a confirmation dialog with Yes/No options.
        
        Params: 
            message: The message to display.
        Return: 
            True if Yes is selected, False otherwise.
        """
        reply = QtWidgets.QMessageBox.question(
            None, self.CONFIRMATION_TITLE, message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        return reply == QtWidgets.QMessageBox.Yes

    def get_file_path(self, save: bool = False) -> str:
        """
        Opens a file dialog to get the file path.
        
        Params: 
            save: True for Save As, False for Open.
        Return: 
            The selected file path or an empty string if canceled.
        """
        if save:
            return QtWidgets.QFileDialog.getSaveFileName(None, "Save As", "", self.FILE_DIALOG_FILTER)[0]
        return QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", self.FILE_DIALOG_FILTER)[0]

    def new_network(self) -> None:
        """
        Clears the current model manager and refreshes the network display.
        """
        if self.show_confirmation_dialog(self.NEW_NETWORK_MESSAGE):
            self.model_manager.reset()
            self.signal_manager.update_visualization_signal.emit()
            SessionState.save({"last_save_path": None})

    def open_file(self) -> None:
        """
        Opens a file and loads it into the model manager.
        """
        path = self.get_file_path(save=False)
        if path:
            try:
                self.model_manager.load(path)
                self.signal_manager.update_visualization_signal.emit()
                
                SessionState.save({"last_save_path": path})
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Failed to open file: {e}")

    def save(self) -> None:
        """
        Saves the current model manager to the current path or prompts for a path if not set.
        """
        session_state = SessionState.load()
        save_path = session_state.get("last_save_path")
        if not save_path:
            self.save_as()
        else:
            try:
                self.model_manager.save(save_path)
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Failed to save file: {e}")

    def save_as(self) -> None:
        """
        Saves the current model manager to a new file.
        """
        path = self.get_file_path(save=True)
        if path:
            try:
                self.model_manager.save(path)
                SessionState.save({"last_save_path": path})
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Failed to save file: {e}")

    def close_main_window(self) -> None:
        """
        Closes the main window after user confirmation.
        """
        if self.show_confirmation_dialog(self.CLOSE_MESSAGE):
            QtWidgets.qApp.quit()

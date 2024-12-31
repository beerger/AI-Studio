from PyQt5 import QtWidgets
from utils.session_state import SessionState
from core.model_manager import ModelManager
from core.signal_manager import SignalManager

class EditController:
    
    def __init__(self, signal_manager: SignalManager):
        self.model_manager = ModelManager()
        self.signal_manager = signal_manager
        self.default_settings = {'show': True, 'zoom': 1, 'dark_mode': False, 'scrollbars': True, 'highlight_connections': True}
        self.current_settings = self.default_settings.copy()
        self.setup_connections()

    def setup_connections(self) -> None:
        self.signal_manager.undo_signal.connect(self.undo)
        self.signal_manager.redo_signal.connect(self.redo)
        self.signal_manager.duplicate_signal.connect(self.duplicate)
        self.signal_manager.remove_last_signal.connect(self.remove_last)
        self.signal_manager.edit_signal.connect(self.edit)
        
    def undo(self) -> None:
        """
        Undoes the last action.
        """
        self.model_manager.undo()
        self.signal_manager.update_visualization_signal.emit()
    
    def redo(self) -> None:
        """
        Redoes the last action.
        """
        self.model_manager.redo()
        self.signal_manager.update_visualization_signal.emit()
    
    def duplicate(self) -> None:
        """
        Duplicates the selected component.
        """
        self.model_manager.duplicate_last_component()
        self.signal_manager.update_visualization_signal.emit()
    
    def remove_last(self) -> None:
        """
        Removes the selected component.
        """
        self.model_manager.remove_last_component()
        self.signal_manager.update_visualization_signal.emit()
    
    def edit(self) -> None:
        """
        Edits the selected component.
        """
        pass

from PyQt5 import QtWidgets
from utils.session_state import SessionState
from core.model_manager import ModelManager
from core.signal_manager import SignalManager

class ViewController:
    
    def __init__(self, signal_manager: SignalManager):
        self.model_manager = ModelManager()
        self.signal_manager = signal_manager
        self.default_settings = {'show': True, 'zoom': 1, 'dark_mode': False, 'scrollbars': True, 'highlight_connections': True}
        self.current_settings = self.default_settings.copy()
        self.setup_connections()

    def setup_connections(self) -> None:
        self.signal_manager.show_hide_signal.connect(self.show_hide_network)
        self.signal_manager.zoom_in_signal.connect(self.zoom_in)
        self.signal_manager.zoom_out_signal.connect(self.zoom_out)
        self.signal_manager.reset_signal.connect(self.reset)
        self.signal_manager.dark_mode_signal.connect(self.dark_mode)
        self.signal_manager.scrollbars_signal.connect(self.scrollbars)
        self.signal_manager.highlight_connections_signal.connect(self.highlight_connections)

    def show_hide_network(self) -> None:
        """
        Toggles the visibility of the network visualization.
        """
        self.current_settings['show'] = not self.current_settings['show']
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def zoom_in(self) -> None:
        """
        Zooms in on the network visualization.
        """
        zoom = min(5, self.current_settings['zoom'] + 0.1) # Ensure zoom is at most 5
        self.current_settings['zoom'] = zoom
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def zoom_out(self) -> None:
        """
        Zooms out on the network visualization.
        """
        zoom = max(0.2, 0, self.current_settings['zoom'] - 0.1) # Ensure zoom is at least 0.2
        self.current_settings['zoom'] = zoom
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def reset(self) -> None:
        """
        Resets the network visualization.
        """
        self.current_settings = self.default_settings.copy()
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def dark_mode(self) -> None:
        """
        Toggles dark mode.
        """
        self.current_settings['dark_mode'] = not self.current_settings['dark_mode']
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def scrollbars(self) -> None:
        """
        Toggles scrollbars.
        """
        self.current_settings['scrollbars'] = not self.current_settings['scrollbars']
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
    
    def highlight_connections(self) -> None:
        """
        Toggles the visibility of connections.
        """
        self.current_settings['highlight_connections'] = not self.current_settings['highlight_connections']
        self.signal_manager.visualization_settings_signal.emit(self.current_settings)
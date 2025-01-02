
from ui.tabs.base_tab import BaseTab

tab_dictionary = {
    'Network Display': [
        {'name': 'Show/Hide Network', 'icon': 'show_hide.png', 'signal': 'show_hide_signal'},
        {'name': 'Highlight Connections', 'icon': 'highlight_connections.png', 'signal': 'highlight_connections_signal'},
    ],
    'Zoom': [
        {'name': 'Zoom In', 'icon': 'zoom_in.png', 'signal': 'zoom_in_signal'},
        {'name': 'Zoom Out', 'icon': 'zoom_out.png', 'signal': 'zoom_out_signal'},
        {'name': 'Reset', 'icon': 'reset.png', 'signal': 'reset_signal'},
    ],
    'Appearance': [
        {'name': 'Dark mode', 'icon': 'dark_mode.png', 'signal': 'dark_mode_signal'},
        {'name': 'Scrollbars', 'icon': 'scrollbars.png', 'signal': 'scrollbars_signal'},
    ],
}

class ViewTab(BaseTab):
    
    def __init__(self, signal_manager, scaling_factor=1.0, parent=None):
        super(ViewTab, self).__init__(signal_manager, scaling_factor, tab_dictionary, parent)
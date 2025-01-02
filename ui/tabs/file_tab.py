from ui.tabs.base_tab import BaseTab

tab_dictionary = {
    'File': [
            {'name': 'New', 'icon': 'new.png', 'signal': 'new_signal'},
            {'name': 'Open', 'icon': 'open.png', 'signal': 'open_signal'},
            {'name': 'Save', 'icon': 'save.png', 'signal': 'save_signal'},
            {'name': 'Save As', 'icon': 'save_as.png', 'signal': 'save_as_signal'},
        ],
    'Application': [{'name': 'Close', 'icon': 'close.png', 'signal': 'close_signal'}],
}

class FileTab(BaseTab):
    
    def __init__(self, signal_manager, scaling_factor=1.0, parent=None):
        super(FileTab, self).__init__(signal_manager, scaling_factor, tab_dictionary, parent)

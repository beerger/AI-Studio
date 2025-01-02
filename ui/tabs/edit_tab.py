from ui.tabs.base_tab import BaseTab

tab_dictionary = {
    'Edit': [{'name': 'Undo', 'icon': 'undo.png', 'signal': 'undo_signal'},
             {'name': 'Redo', 'icon': 'redo.png', 'signal': 'redo_signal'},
             {'name': 'Duplicate Component', 'icon': 'duplicate.png', 'signal': 'duplicate_signal'},
             {'name': 'Remove Component', 'icon': 'placeholder.png', 'signal': 'remove_last_signal'},
             {'name': 'Edit Parameters', 'icon': 'edit.png', 'signal': 'edit_signal'}
             ]
}

class EditTab(BaseTab):
    def __init__(self, signal_manager, scaling_factor=1.0, parent=None):
        super(EditTab, self).__init__(signal_manager, scaling_factor, tab_dictionary, parent)
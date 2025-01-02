from ui.tabs.base_tab import BaseTab


tab_dictionary = {
    'Tools': [{'name': 'Validate Network', 'icon': 'validate_network.png', 'signal': 'validate_network_signal'},
              {'name': 'Generate Summary', 'icon': 'generate_summary.png', 'signal': 'generate_summary_signal'},
              {'name': 'Import Model', 'icon': 'import_pretrained.png', 'signal': 'import_pretrained_signal'},
              {'name': 'Export to ONNX', 'icon': 'export_onnx.png', 'signal': 'export_onnx_signal'},
              {'name': 'Generate code', 'icon': 'generate_code.png', 'signal': 'generate_code_signal'},
              ],
}

class ToolsTab(BaseTab):
    
    def __init__(self, signal_manager, scaling_factor=1.0, parent=None):
        super(ToolsTab, self).__init__(signal_manager, scaling_factor, tab_dictionary, parent)
from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):

    ########## Tab signals ##########
    
    # File tab signals
    new_signal = pyqtSignal()
    open_signal = pyqtSignal()
    save_signal = pyqtSignal()
    save_as_signal = pyqtSignal()
    close_signal = pyqtSignal()
    
    # View tab signals
    show_hide_signal = pyqtSignal()
    zoom_in_signal = pyqtSignal()
    zoom_out_signal = pyqtSignal()
    reset_signal = pyqtSignal()
    dark_mode_signal = pyqtSignal()
    scrollbars_signal = pyqtSignal()
    highlight_connections_signal = pyqtSignal()
    
    # Edit tab signals
    undo_signal = pyqtSignal()
    redo_signal = pyqtSignal()
    duplicate_signal = pyqtSignal()
    remove_last_signal = pyqtSignal()
    edit_signal = pyqtSignal()
    
    # Tools tab signals
    validate_network_signal = pyqtSignal()
    generate_summary_signal = pyqtSignal()
    import_pretrained_signal = pyqtSignal()
    export_onnx_signal = pyqtSignal()
    generate_code_signal = pyqtSignal()
    
    ########## Network signals ##########
    visualization_settings_signal = pyqtSignal(dict)
    component_added_signal = pyqtSignal(dict)
    update_visualization_signal = pyqtSignal()

    apply_scaling = pyqtSignal(float)
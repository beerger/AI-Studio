from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    
    ############ File tab signals ############
    
    #### File ####
    new_signal = pyqtSignal()
    open_signal = pyqtSignal()
    save_signal = pyqtSignal()
    save_as_signal = pyqtSignal()
    close_signal = pyqtSignal()
    
    component_added_signal = pyqtSignal(dict)
    components_updated_signal = pyqtSignal(dict)
    update_visualization_signal = pyqtSignal(object)
    
    
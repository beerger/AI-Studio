from PyQt5 import QtWidgets

class ConfigurationTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ConfigurationTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Configuration Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
    
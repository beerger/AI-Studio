from PyQt5 import QtWidgets

class SettingsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingsTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Settings Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

from PyQt5 import QtWidgets

class DebugTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DebugTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Debug Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
    
from PyQt5 import QtWidgets

class ToolsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ToolsTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Tools Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
    
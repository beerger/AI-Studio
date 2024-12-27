from PyQt5 import QtWidgets

class HelpTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HelpTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Help Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
    
from PyQt5 import QtWidgets

class RunTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RunTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Run Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)
    
from PyQt5 import QtWidgets

class EditTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EditTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('Edit Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

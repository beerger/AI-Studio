from PyQt5 import QtWidgets

class ViewTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ViewTab, self).__init__(parent)
        self.button = QtWidgets.QPushButton('View Tab')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

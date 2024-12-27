from PyQt5 import QtWidgets
from PyQt5 import QtCore

class FileTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FileTab, self).__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        
        self.setup_actions(['New', 'Open', 'Save', 'Save As'], 'File')
        self.setup_actions(['Close', 'Close All'], 'Close')
        self.setup_actions(['Exit'], 'Exit')
        
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(horizontal_spacer)

    def setup_actions(self, actions, category):
        """
        Creates a vertical layout with buttons for each action and a label for the category.
        params:
            actions: list of actions
            category: category of actions
        """
        v_layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        for action in actions:
            button = QtWidgets.QPushButton(action)
            h_layout.addWidget(button)
        v_layout.addLayout(h_layout)
        label = QtWidgets.QLabel(category)
        label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        v_layout.addWidget(label)
        self.main_layout.addLayout(v_layout)
        vertical_line = QtWidgets.QFrame()
        vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
        vertical_line.setStyleSheet('color: lightGray')
        self.main_layout.addWidget(vertical_line)
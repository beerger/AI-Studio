from ui.popups.frameless_popup import FrameLessPopup
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout
from PyQt5 import QtGui
from utils.file_helper import ICON_DIR
import os
from PyQt5 import QtCore

class CustomMessageBox(FrameLessPopup):
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    QUESTION = "question"

    def __init__(self, title, message, message_type=INFO, parent=None):
        super().__init__(parent, vertical_layout=False)
        self.title_label.setText(title)

        # Icon based on the message type
        self.icon_label = QLabel(self)
        if message_type == self.WARNING:
            icon = "warning.png"
        elif message_type == self.ERROR:
            icon = "error.png"
        elif message_type == self.INFO:
            icon = "info.png"
        elif message_type == self.QUESTION:
            icon = "question.png"
        else:
            icon = None

        if icon:
            icon_path = os.path.join(ICON_DIR, icon)
            pixmap = QtGui.QPixmap(icon_path)
            if not pixmap.isNull():
                # Resize the pixmap to 32x32
                pixmap = pixmap.scaled(32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.icon_label.setPixmap(pixmap)
                self.content_layout.addWidget(self.icon_label)

        # Add the message
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.content_layout.addWidget(self.message_label)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        self.content_layout.addLayout(self.button_layout)

        self.setMinimumSize(300, 150)

    @staticmethod
    def warning(parent, title, message):
        dialog = CustomMessageBox(title, message, message_type=CustomMessageBox.WARNING, parent=parent)
        return dialog.exec_()

    @staticmethod
    def error(parent, title, message):
        dialog = CustomMessageBox(title, message, message_type=CustomMessageBox.ERROR, parent=parent)
        return dialog.exec_()

    @staticmethod
    def info(parent, title, message):
        dialog = CustomMessageBox(title, message, message_type=CustomMessageBox.INFO, parent=parent)
        return dialog.exec_()

    @staticmethod
    def question(parent, title, message):
        dialog = CustomMessageBox(title, message, message_type=CustomMessageBox.QUESTION, parent=parent)
        dialog.ok_button.setText("Yes")
        dialog.cancel_button = QPushButton("No")
        dialog.cancel_button.clicked.connect(dialog.reject)
        dialog.button_layout.addWidget(dialog.cancel_button)
        return dialog.exec_()
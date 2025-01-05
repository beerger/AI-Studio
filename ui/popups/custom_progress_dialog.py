
from ui.popups.frameless_popup import FrameLessPopup
from PyQt5.QtWidgets import QLabel, QProgressBar, QPushButton
from PyQt5.QtWidgets import QApplication
# import signals
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

class CustomProgressDialog(FrameLessPopup):
    canceled = pyqtSignal()
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.title_label.setText(title)
        self._allow_close = False

        # Add the message
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.content_layout.addWidget(self.message_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("customProgressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.content_layout.addWidget(self.progress_bar)
        
        # Add cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.content_layout.addWidget(self.cancel_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.setMinimumSize(300, 150)

    def setValue(self, value):
        print(f"Setting value: {value}")
        self.progress_bar.setValue(value)
        QApplication.processEvents()
        if value >= 100:
            self._allow_close = True
            self.close()

    def closeEvent(self, event):
        if self._allow_close:
            event.accept()  # Allow closing
        else:
            event.ignore()  # Prevent closing
        
    def close_safely(self):
      if not self._allow_close:
        self._allow_close = True
        self.close()
    
    def on_cancel(self):
        self.canceled.emit()
        self._allow_close = True  # Allow the dialog to close
        self.close()

    @staticmethod
    def show(parent, title, message):
        dialog = CustomProgressDialog(title, message, parent=parent)
        return dialog
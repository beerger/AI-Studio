from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtCore import pyqtSignal

class MenuBar(QMenuBar):
    
    new_signal = pyqtSignal()
    open_signal = pyqtSignal()
    save_signal = pyqtSignal()
    save_as_signal = pyqtSignal()
    generate_code_signal = pyqtSignal()
    close_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # File Menu
        self.menuFile = QMenu("File", self)
        self.addMenu(self.menuFile)

        # Actions
        self.actionNew = QAction("New", self)
        self.actionOpen = QAction("Open", self)
        self.actionSave = QAction("Save", self)
        self.actionSave_as = QAction("Save As", self)
        self.actionGenerate_Code = QAction("Generate Code", self)
        self.actionClose = QAction("Close", self)

        # Add actions to the File menu
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionGenerate_Code)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        # Connect actions
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open_)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionGenerate_Code.triggered.connect(self.generate_code)
        self.actionClose.triggered.connect(self.emit_close_signal)
        
    def new(self):
        self.new_signal.emit()

    def open_(self):
        self.open_signal.emit()
        
    def save(self):
        self.save_signal.emit()
        
    def save_as(self):
        self.save_as_signal.emit()
        
    def generate_code(self):
        print("Not implemented yet.")
        
    def generate_code(self):
        self.generate_code_signal.emit()
        
    def emit_close_signal(self):
        self.close_signal.emit()
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from utils.session_state import SessionState
import utils.file_helper as file_helper
from ui.network import Network
from ui.component_layout import ComponentLayoutWidget
from ui.tab_manager import TabManager
from ui.controllers.file_controller import FileController
from ui.controllers.view_controller import ViewController
from ui.controllers.edit_controller import EditController
from ui.controllers.tools_controller import ToolsController
from core.components import WRAPPER_REGISTRY
from core.signal_manager import SignalManager
from core.model_manager import ModelManager
from core.shortcut_handler import ShortcutHandler
from styling.color_scheme import ColorScheme
import os

class Ui_MainWindow(QObject):
    
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager.load_from_session_state(SessionState())
        self.signal_manager = SignalManager()
        self.setup_controllers()
        
    def setupUi(self, MainWindow):
        """
        Sets up the main window layout, components, and functionality.
        """
        self.init_main_window(MainWindow)
        self.init_layout(MainWindow)
        self.init_status_bar(MainWindow)
        self.setup_shortcuts() # Requires centralwidget to be set
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_main_window(self, MainWindow):
        """
        Initializes the main window properties.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, 2000, 600))
        MainWindow.showMaximized()

        # Set the window icon
        icon = file_helper.create_icon('company_logo.png')
        MainWindow.setWindowIcon(icon)

    def init_layout(self, MainWindow):
        """
        Sets up the main layout and adds widgets.
        """
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setContentsMargins(0, 0, 0, 0) # Remove central widget margins
        
        # Main vertical layout
        main_v_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_v_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        main_v_layout.setSpacing(0)  # Remove spacing
        
        # Tab manager widget
        self.tab_manager = TabManager(self.signal_manager)
        main_v_layout.addWidget(self.tab_manager, stretch=0)
        
        # Horizontal layout
        h_layout = QtWidgets.QHBoxLayout()

        component_dock_widget = QtWidgets.QDockWidget(self.centralwidget)
        # Component layout widget
        component_layout_widget = ComponentLayoutWidget(self.signal_manager)
        component_dock_widget.setWidget(component_layout_widget)
        
        h_layout.addWidget(component_dock_widget, stretch=1)

        # Add network visualization widget
        self.network = Network(self.signal_manager)
        h_layout.addWidget(self.network, stretch=10)
        
        main_v_layout.addLayout(h_layout, stretch=10)

        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, component_dock_widget)
        MainWindow.setCentralWidget(self.centralwidget)

    def init_status_bar(self, MainWindow):
        """
        Initializes the status bar.
        """
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignRight)
        label = QtWidgets.QLabel("AI Studio")
        layout.addWidget(label)
        self.statusbar.addPermanentWidget(label)
        
    def setup_controllers(self):
        self.file_controller = FileController(self.signal_manager)
        self.view_controller = ViewController(self.signal_manager)
        self.edit_controller = EditController(self.signal_manager)
        self.tools_controller = ToolsController(self.signal_manager)
        
    def setup_shortcuts(self):
        shortcut_map = {
            'Ctrl+N': self.file_controller.new_network,
            'Ctrl+O': self.file_controller.open_file,
            'Ctrl+S': self.file_controller.save,
            'Ctrl+Shift+S': self.file_controller.save_as,
            'Ctrl+Q': self.file_controller.close_main_window,
            'Ctrl++': self.view_controller.zoom_in,
            'Ctrl+-': self.view_controller.zoom_out,
            'Ctrl+R': self.view_controller.reset,
            'Ctrl+Z': self.edit_controller.undo,
            'Ctrl+Y': self.edit_controller.redo,
        }
        self.shortcut_handler = ShortcutHandler(self.centralwidget, shortcut_map)
        
    def retranslateUi(self, MainWindow):
        """
        Sets up the text and titles for the UI components.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("AI studio", "AI studio"))
    
    def closeEvent(self, event):
        """
        Override the close event to prompt the user to save before closing.
        """
        print("close event called")
        self.file_controller.close_main_window(event)
        
    def wheelEvent(self, event):
        """
        Override the wheel event to zoom in and out.
        """
        # Zoom in or out
        if event.angleDelta().y() > 0:
            self.view_controller.zoom_in()
        else:
            self.view_controller.zoom_out()
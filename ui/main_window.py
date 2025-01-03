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
import os

class Ui_MainWindow(QObject):
    
    def __init__(self, dpi=96, scaling_factor=1.0, signal_manager=None):
        super().__init__()
        self.dpi = dpi
        self.scaling_factor = scaling_factor
        self.model_manager = ModelManager.load_from_session_state(SessionState())
        self.signal_manager = signal_manager if signal_manager else SignalManager()
        self.setup_controllers()
        
    def setupUi(self, MainWindow):
        """
        Sets up the main window layout, components, and functionality.
        """
        self.init_main_window(MainWindow)
        self.init_layout(MainWindow)
        self.init_status_bar(MainWindow)
        self.setup_shortcuts() # Requires centralwidget to be set
        
        # Apply the theme after setting up the UI
        theme_file = os.path.join("themes", "standard_theme.qss")
        self.apply_theme(theme_file)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_main_window(self, MainWindow):
        """
        Initializes the main window properties.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, int(2000 * self.scaling_factor), int(600 * self.scaling_factor)))
        MainWindow.showMaximized()

        # Set the window icon
        icon = file_helper.create_icon('company_logo.png')
        MainWindow.setWindowIcon(icon)
        
    def apply_theme(self, theme_file):
        with open(theme_file, 'r') as f:
            style = f.read()
        QtWidgets.QApplication.instance().setStyleSheet(style)

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
        self.tab_manager = TabManager(self.signal_manager, scaling_factor=self.scaling_factor)
        self.tab_manager.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_v_layout.addWidget(self.tab_manager, stretch=1) # stretch=1
        
        components_dock_widget = QtWidgets.QDockWidget(self.centralwidget)
        components_widget = ComponentLayoutWidget(self.signal_manager)
        components_dock_widget.setWidget(components_widget)
        components_dock_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        # Layout for the component dock widget and network visualization
        dock_network_layout = QtWidgets.QHBoxLayout()
        dock_network_layout.addWidget(components_dock_widget, stretch=1) 

        # Add network visualization widget
        self.network = Network(self.signal_manager)
        self.network.wheelEvent = self.wheelEvent  # Override wheel event
        self.network.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        dock_network_layout.addWidget(self.network, stretch=4)
        
        main_v_layout.addLayout(dock_network_layout, stretch=9) # stretch=9

        
        # Dock for dataloader
        dataloader_dock_widget = QtWidgets.QDockWidget(self.centralwidget)
        dataloader_widget = QtWidgets.QLabel("Dataloader")
        dataloader_dock_widget.setWidget(dataloader_widget)
        
        # Dock for configuration
        configuration_dock_widget = QtWidgets.QDockWidget(self.centralwidget)
        configuration_widget = QtWidgets.QLabel("Configuration")
        configuration_dock_widget.setWidget(configuration_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, components_dock_widget)
        MainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, dataloader_dock_widget)
        MainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, configuration_dock_widget)

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
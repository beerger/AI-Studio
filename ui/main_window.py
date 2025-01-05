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
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

class Ui_MainWindow(QObject):
    
    def __init__(self, dpi=96, scaling_factor=1.0, signal_manager=None):
        super().__init__()
        self.dpi = dpi
        self.scaling_factor = scaling_factor
        self.model_manager = ModelManager.load_from_session_state(SessionState())
        self.signal_manager = signal_manager if signal_manager else SignalManager()
        self.setup_controllers()
        self.dragging = False # Track dragging state for frameless window
        
    def setupUi(self, MainWindow):
        """
        Sets up the main window layout, components, and functionality.
        """
        self.init_main_window(MainWindow)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)

        # Main vertical layout
        self.main_v_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        # Add custom title bar
        self.add_custom_title_bar(MainWindow)

        # Add the rest of the layout
        self.init_layout(MainWindow)

        # Initialize other components
        self.init_status_bar(MainWindow)
        self.setup_shortcuts()

        # Apply the theme after setting up the UI
        theme_file = os.path.join("themes", "standard_theme", "standard_theme_generated.qss")
        self.apply_theme(theme_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_main_window(self, MainWindow):
        """
        Initializes the main window properties.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setGeometry(QtCore.QRect(0, 0, int(1200 * self.scaling_factor), int(600 * self.scaling_factor)))
        MainWindow.showMaximized()

        #cursor_pixmap = QtGui.QPixmap("D:/OneDrive - Uppsala universitet/General/AI-Studio/resources/icons/cursor_3d.png")
        #scaled_cursor_pixmap = cursor_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #custom_cursor = QtGui.QCursor(scaled_cursor_pixmap, 0, 0)  # Hotspot at top-left corner
        #MainWindow.setCursor(custom_cursor)
        # Set the window icon
        icon = file_helper.create_icon('company_logo.png')
        MainWindow.setWindowIcon(icon)
        
    def apply_theme(self, theme_file):
        with open(theme_file, 'r') as f:
            style = f.read()
        QtWidgets.QApplication.instance().setStyleSheet(style)
        
        
    def add_custom_title_bar(self, MainWindow):
        """
        Adds a custom title bar with minimize, maximize, and close buttons.
        """
        self.main_window = MainWindow  # Store the reference to MainWindow
        self.title_bar = QtWidgets.QWidget()
        #call toggle_maximize when double click on title bar
        self.title_bar.mouseDoubleClickEvent = self.toggle_maximize
        
        self.title_bar.setObjectName("titleBar")
        self.title_bar_layout = QtWidgets.QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(10, 0, 10, 0)
    
        # Add title
        self.title_icon = QtWidgets.QLabel()
        icon = file_helper.create_icon('company_logo.png')
        self.title_icon.setPixmap(icon.pixmap(16, 16))
        self.title_icon.setStyleSheet("background-color: transparent;")
        self.title_bar_layout.addWidget(self.title_icon, alignment=QtCore.Qt.AlignLeft)
        

        self.titel_label = QtWidgets.QLabel("AI Studio")
        self.titel_label.setObjectName("titleLabel")
        self.title_bar_layout.addWidget(self.titel_label, alignment=QtCore.Qt.AlignLeft)
        
        # Add a spacer to push buttons to the right
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.title_bar_layout.addSpacerItem(spacer)
        
        # Add buttons
        self.minimize_button = QtWidgets.QPushButton("-")
        self.minimize_button.setObjectName("titleBarButton")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.clicked.connect(self.main_window.showMinimized)
    
        self.maximize_button = QtWidgets.QPushButton("+")
        self.maximize_button.setObjectName("titleBarButton")
        
        self.maximize_button.setFixedSize(20, 20)
        self.maximize_button.clicked.connect(self.toggle_maximize)
    
        self.close_button = QtWidgets.QPushButton("x")
        self.close_button.setObjectName("titleBarButton")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.main_window.close)

        self.title_bar_layout.addWidget(self.minimize_button, alignment=QtCore.Qt.AlignRight)
        self.title_bar_layout.addWidget(self.maximize_button, alignment=QtCore.Qt.AlignRight)
        self.title_bar_layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)
    
        # Enable dragging
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag
        self.title_bar.mouseReleaseEvent = self.stop_drag
    
        # Add the title bar to the main layout
        self.main_v_layout.addWidget(self.title_bar, stretch=2)

        
    def start_drag(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.main_window.frameGeometry().topLeft()
            event.accept()

    def perform_drag(self, event):
        if self.dragging and event.buttons() == QtCore.Qt.LeftButton:
            self.main_window.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def stop_drag(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            event.accept()

            
    def toggle_maximize(self, event):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            print("show max")
            self.main_window.showMaximized()

    def init_layout(self, MainWindow):
        """
        Sets up the main layout and adds widgets.
        """
        # Tab manager widget
        self.tab_manager = TabManager(self.signal_manager, scaling_factor=self.scaling_factor)
        self.tab_manager.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.main_v_layout.addWidget(self.tab_manager, stretch=10)  # Add tab manager below title bar

        # Components dock widget
        components_dock_widget = QtWidgets.QDockWidget(self.centralwidget)
        components_widget = ComponentLayoutWidget(self.signal_manager)
        components_dock_widget.setWidget(components_widget)
        components_dock_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        components_dock_widget.setMinimumSize(QtCore.QSize(200, 200))
        components_dock_widget.setMaximumSize(QtCore.QSize(1000, 1000))

        # Layout for the component dock widget and network visualization
        dock_network_layout = QtWidgets.QHBoxLayout()
        dock_network_layout.addWidget(components_dock_widget, stretch=1)

        # Add network visualization widget
        self.network = Network(self.signal_manager)
        self.network.wheelEvent = self.wheelEvent  # Override wheel event
        self.network.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        dock_network_layout.addWidget(self.network, stretch=4)

        # Add layout to the main layout
        dock_network_widget = QtWidgets.QWidget()
        dock_network_widget.setLayout(dock_network_layout)
        self.main_v_layout.addWidget(dock_network_widget, stretch=90)

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

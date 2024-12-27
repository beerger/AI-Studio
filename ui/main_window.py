from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QRect
import torch.nn as nn
from core.module import ModelManager, WRAPPER_REGISTRY
from core.code_generator import CodeGenerator
from ui.network import Network
from ui.component_layout import ComponentLayoutWidget
from ui.menu_bar import MenuBar
from utils.file_helper import get_absolute_path
from utils.session_state import SessionState
from ui.tab_manager import TabManager
import os


class Ui_MainWindow(QObject):
    component_list_updated_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager()
        self.current_save_path = None
        self.load_session_state()
        
    def load_session_state(self):
        # Load session state
        session_state = SessionState.load()
        self.current_save_path = session_state.get("last_save_path")
        if self.current_save_path and not session_state.get("is_new_network", True):
            self.model_manager = ModelManager.load(self.current_save_path)

    def setupUi(self, MainWindow):
        """
        Sets up the main window layout, components, and functionality.
        """
        self.init_main_window(MainWindow)
        self.init_layout(MainWindow)
        self.init_menu(MainWindow)
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
        icon = self.create_icon('assets', 'company_logo.png')
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
        
        
        self.tab_manager = TabManager(self.centralwidget)
        main_v_layout.addWidget(self.tab_manager, stretch=0)
        
        
        # Horizontal layout
        h_layout = QtWidgets.QHBoxLayout()

        # Component layout widget
        component_layout_widget = ComponentLayoutWidget()
        component_layout_widget.component_added_signal.connect(self.handle_component_added)
        h_layout.addWidget(component_layout_widget)

        # Add network visualization widget
        self.network = Network(self.model_manager)
        self.component_list_updated_signal.connect(self.network.handle_component_list_update)
        h_layout.addWidget(self.network, stretch=10)
        
        main_v_layout.addLayout(h_layout, stretch=10)

        MainWindow.setCentralWidget(self.centralwidget)

    def init_menu(self, MainWindow):
        """
        Initializes the menu bar and status bar.
        """
        pass
        #self.tab_manager = TabManager()
        #self.menubar = MenuBar(MainWindow)
        #MainWindow.setMenuBar(self.menubar)
        #self.menubar.new_signal.connect(self.new_network)
        #self.menubar.open_signal.connect(self.open_file)
        #self.menubar.save_signal.connect(self.save)
        #self.menubar.save_as_signal.connect(self.save_as)
        #self.menubar.generate_code_signal.connect(self.generate_code)
        #self.menubar.close_signal.connect(self.close_main_window)
        #
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #MainWindow.setStatusBar(self.statusbar)
    
    def create_icon(self, *path_parts):
        """
        Creates a QIcon from the given path parts.
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(get_absolute_path(*path_parts)), QtGui.QIcon.Selected, QtGui.QIcon.On)
        return icon

    def create_label_with_image(self, *path_parts):
        """
        Creates a QLabel with a specified image.
        """
        label = QtWidgets.QLabel(self.centralwidget)
        label.setPixmap(QtGui.QPixmap(get_absolute_path(*path_parts)))
        return label

    def handle_component_added(self, component_data):
        """
        Handles the component_added_signal signal from ComponentLayoutWidget.
        """
        args = component_data.get('args')
        name = component_data.get('name')
        wrapper_class = WRAPPER_REGISTRY.get(name)
        if not wrapper_class:
            raise NotImplementedError(f"Wrapper class for {name} not found.")
        # Instantiate the wrapper and add it to the model manager
        component = wrapper_class(name, args)
        self.model_manager.add_component(component)
        self.component_list_updated_signal.emit(self.model_manager)
        
    def new_network(self):
        """
        Clears the current model manager and refreshes the network display.
        """
        reply = QtWidgets.QMessageBox.question(None, "New Network", "Are you sure you want to start a new network?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.model_manager = ModelManager()
            self.component_list_updated_signal.emit(self.model_manager)
            self.current_save_path = None
            SessionState.save({
            "last_save_path": None,
            "is_new_network": True
        })
    
    def open_file(self):
        """
        Opens a file and loads the model manager.
        """
        path = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "", "Pickle Files (*.pkl)")[0]
        if path:
            self.model_manager = ModelManager.load(path)
            self.component_list_updated_signal.emit(self.model_manager)
            self.current_save_path = path
            SessionState.save({
            "last_save_path": path,
            "is_new_network": False
        })

    def save(self):
        """
        Saves the current model manager to the current path.
        """
        if not self.current_save_path:
            self.save_as()
        else:
            self.model_manager.save(self.current_save_path)

    def save_as(self):
        """
        Saves the current model manager to a file.
        """
        path = QtWidgets.QFileDialog.getSaveFileName(None, "Save As", "", "Pickle Files (*.pkl)")[0]
        if path:
            self.current_save_path = path
            self.model_manager.save(path)
            SessionState.save({
            "last_save_path": path,
            "is_new_network": False
        })
    
    def generate_code(self):
        """
        Generates code for the current model manager.
        """
        code_generator = CodeGenerator(self.model_manager, "generated_code")
        code_generator.generate_all()
    
    def close_main_window(self):
        """
        Closes the main window.
        """
        SessionState.save({
            "last_save_path": self.current_save_path,
            "is_new_network": self.current_save_path is None
        })
        QtWidgets.qApp.quit()
        
    def retranslateUi(self, MainWindow):
        """
        Sets up the text and titles for the UI components.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("AI studio", "AI studio"))
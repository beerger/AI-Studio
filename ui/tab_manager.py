from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QBrush, QColor, QFont
from ui.tabs.file_tab import FileTab
from ui.tabs.edit_tab import EditTab
from ui.tabs.view_tab import ViewTab
from ui.tabs.tools_tab import ToolsTab
from ui.tabs.configuration_tab import ConfigurationTab
from ui.tabs.run_tab import RunTab
from ui.tabs.help_tab import HelpTab
from ui.tabs.debug_tab import DebugTab
from core.signal_manager import SignalManager
from styling.color_scheme import ColorScheme

class TabManager(QtWidgets.QWidget):
    
    model_manager_updated_signal = pyqtSignal(object)
    TAB_COLOR_Q = QColor(0, 64, 115, 255)  # Blue color
    TAB_COLOR_RGBA = "rgba(0, 64, 115, 255)"
    
    def __init__(self, signal_manager: SignalManager, parent=None):
        super(TabManager, self).__init__(parent)
        self.signal_manager = signal_manager
        self.init_ui()
        self.setAutoFillBackground(True)
        parent_palette = self.palette()
        parent_palette.setColor(self.backgroundRole(), self.TAB_COLOR_Q)  # Blue background
        self.setPalette(parent_palette)

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing
        
        self.tab = QtWidgets.QTabWidget()
        self.tab.setMovable(True)
        
        # Set a fixed height for the tab menu
        # This is necessary to prevent the tab menu from resizing when changing main window size
        self.tab.setFixedHeight(200) # TODO: Calculate based on screen size
        
        # Add tabs
        self.tab.addTab(FileTab(self.signal_manager), "FILE")
        self.tab.addTab(EditTab(self.signal_manager), "EDIT")
        self.tab.addTab(ViewTab(self.signal_manager), "VIEW")
        self.tab.addTab(ToolsTab(self.signal_manager), "TOOLS")
        self.tab.addTab(ConfigurationTab(), "CONFIGURATION")
        self.tab.addTab(RunTab(), "RUN")
        self.tab.addTab(HelpTab(), "HELP")
        self.tab.addTab(DebugTab(), "DEBUG")
        self.layout.addWidget(self.tab)
        
        self.apply_stylesheet()
        

    def apply_stylesheet(self):
        """Apply the stylesheet with dynamically calculated tab width."""
        # TODO: Pane color should not be hard coded (is currently same as the rest of the window color)
        font = self.tab.font()
        font.setPointSize(18)
        self.tab.setFont(font)
        tab_width = self.calculate_tab_width()
        self.tab.setStyleSheet(f"""
        QTabWidget::pane {{
            background-color: rgba(240, 240, 240, 255);
            border: 0px solid lightGray;
            border-bottom: 1px solid #828790; /* Add top border to the pane */
        }}
        QTabBar {{
            background-color: {self.TAB_COLOR_RGBA}; /* Tab bar background */
        }}
            QTabBar::tab {{
                background: {self.TAB_COLOR_RGBA}; /* Tab color */
                color: white;
                min-width: {tab_width}px;
                max-width: {tab_width}px;
                font-size: 18px;
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 10px;
                padding-bottom: 10px;
                border-top-left-radius: 2px;
                border-top-right-radius: 2px;
                margin-top: 5px;
                margin-right: 4px;
                margin-left: 1px;
            }}
            
            QTabBar::tab:selected {{
                background: rgba(240, 240, 240, 255); /* Selected tab color */
                color: black;
            }}

            QTabBar::tab:hover {{
                background: rgba(0, 99, 179, 255); /* Hover color */
            }}
        """)
        
    def calculate_tab_width(self):
        """Calculate the width of the longest tab, scaled for screen DPI."""
        base_width = max(self.tab.fontMetrics().boundingRect(self.tab.tabText(i)).width() for i in range(self.tab.count()))
        print(f"Base width: {base_width}")
        return base_width + 50

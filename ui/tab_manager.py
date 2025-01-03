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

class TabManager(QtWidgets.QWidget):
    
    model_manager_updated_signal = pyqtSignal(object)
    TAB_COLOR_Q = QColor(0, 64, 115, 255)  # Blue color
    TAB_COLOR_RGBA = "rgba(0, 64, 115, 255)"
    
    def __init__(self, signal_manager: SignalManager, scaling_factor=1, parent=None):
        super(TabManager, self).__init__(parent)
        self.signal_manager = signal_manager
        self.scaling_factor = scaling_factor
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
        #self.tab.setFixedHeight(500) # TODO: Calculate based on screen size
        
        # Add tabs
        self.tab.addTab(FileTab(self.signal_manager, self.scaling_factor), "FILE")
        self.tab.addTab(EditTab(self.signal_manager, self.scaling_factor), "EDIT")
        self.tab.addTab(ViewTab(self.signal_manager, self.scaling_factor), "VIEW")
        self.tab.addTab(ToolsTab(self.signal_manager, self.scaling_factor), "TOOLS")
        self.tab.addTab(ConfigurationTab(), "CONFIGURATION")
        self.tab.addTab(RunTab(), "RUN")
        self.tab.addTab(HelpTab(), "HELP")
        self.tab.addTab(DebugTab(), "DEBUG")
        self.layout.addWidget(self.tab)
        
        self.signal_manager.apply_scaling.connect(self.apply_scaling)
        self.apply_stylesheet()
        

    def apply_stylesheet(self):
        """Apply the stylesheet with dynamically calculated tab width."""
        font = self.tab.font()
        font.setPointSize(int(12 * self.scaling_factor))
        self.tab.setFont(font)

        tab_width = self.calculate_tab_width()
        padding = int(7 * self.scaling_factor)
        margin_top = int(3 * self.scaling_factor)
        margin_right = int(3 * self.scaling_factor)
        margin_left = int(5 * self.scaling_factor)
        pane_border = int(self.scaling_factor)
        self.tab.setStyleSheet(f"""
        QTabWidget::pane {{
            background-color: rgba(240, 240, 240, 255);
            border: 0px solid lightGray;
            border-bottom: {min(1, self.scaling_factor)}px solid #828790;
        }}
        QTabBar {{
            background-color: {self.TAB_COLOR_RGBA};
        }}
        QTabBar::tab {{
            background: {self.TAB_COLOR_RGBA};
            color: white;
            min-width: {tab_width}px;
            font-size: {int(12 * self.scaling_factor)}px;
            padding: {padding}px;
            margin-top: {margin_top}px;
            margin-right: {margin_right}px;
            margin-left: {margin_left}px;
            border-top-left-radius: 2px;
            border-top-right-radius: 2px;
        }}
        QTabBar::tab:selected {{
            background: rgba(240, 240, 240, 255);
            color: black;
        }}
        QTabBar::tab:hover {{
            background: rgba(0, 99, 179, 255);
        }}
        """)

        
    def calculate_tab_width(self):
        """Calculate the width of the longest tab, scaled for screen DPI."""
        base_width = max(self.tab.fontMetrics().boundingRect(self.tab.tabText(i)).width() for i in range(self.tab.count()))
        scaled_width = base_width * self.scaling_factor
        return scaled_width

    def apply_scaling(self, scaling_factor):
        print(f"TabManager: Scaling factor updated to {scaling_factor}")
        self.scaling_factor = scaling_factor
        self.apply_stylesheet()
        self.tab.widget(0).apply_scaling(scaling_factor)
        self.tab.widget(1).apply_scaling(scaling_factor)
        self.tab.widget(2).apply_scaling(scaling_factor)
        self.tab.widget(3).apply_scaling(scaling_factor)
        self.update()
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from core.model_manager import ModelManager
from core.signal_manager import SignalManager
from functools import partial

class Network(QtWidgets.QWidget):
    def __init__(self, signal_manager: SignalManager, parent=None):
        super().__init__(parent)
        self.model_manager = ModelManager()
        self.signal_manager = signal_manager
        self.default_settings = {'show': True, 'zoom': 1, 'dark_mode': False, 'scrollbars': True, 'highlight_connections': True}
        self.current_settings = self.default_settings.copy()
        self.setup_connections()
        
        # Timer for debouncing resize events
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.handle_resize)
        
        # Create a scroll area to wrap the layout
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)   
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create a container widget for the layout
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("NetworkContainer")
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.layout = QtWidgets.QHBoxLayout(self.container)
        self.layout.setSpacing(10)  # Adjust spacing between components
        self.scroll_area.setWidget(self.container)

        # Main layout to hold the scroll area
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        # Call render_network to initialize
        self.render_network()
        
    def setup_connections(self) -> None:
        """
        Set up connections for the signal manager.
        """
        self.signal_manager.update_visualization_signal.connect(self.render_network)
        self.signal_manager.visualization_settings_signal.connect(self.render_network)

    def render_network(self, settings=None):
        """
        Renders the network based on the current model manager.
        Adds a line between each component.
        """
        self.current_settings = settings if settings is not None else self.current_settings
        # Clear the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        show = self.current_settings.get('show', True)
        zoom = self.current_settings.get('zoom', 1)
        dark_mode = self.current_settings.get('dark_mode', False) # TODO: Implement dark mode
        scrollbars = self.current_settings.get('scrollbars', True)
        highlight_connections = self.current_settings.get('highlight_connections', False)
                
        if not show:
            self.show_hidden_message()
            return
        
        if len(self.model_manager) == 0:
            self.show_empty_message()
            return
        
        self.scrollbars(scrollbars)

        # Iterate through the components
        for i, component in enumerate(self.model_manager):
            # Add the component's widget
            widget = component.get_widget()
            widget.clicked.connect(lambda _, component=component: print(component.params))
            scaling_factor = widget.scaling_factor if hasattr(widget, 'scaling_factor') else 1
            component_height = int(self.height() * 0.3 * scaling_factor  * zoom)
            component_width = int(self.width() * 0.1 * scaling_factor * zoom)
            widget.setFixedSize(component_width, component_height)
            current_stylesheet = widget.styleSheet()
            font_stylesheet = "font-size: 32px;"
            widget.setStyleSheet(current_stylesheet + font_stylesheet)  # Set the font size
            self.layout.addWidget(widget)

            if highlight_connections:
                # Add a line after each widget, except the last one
                if i < len(self.model_manager) - 1:
                    self.add_line()

        # Add a spacer at the end to ensure proper alignment
        self.layout.addStretch()
        
    def show_hidden_message(self):
        hidden_label = QtWidgets.QLabel("Network is hidden. Click View -> Show/Hide Network to show.")
        self.layout.addWidget(hidden_label)
        # set central alignment
        self.layout.setAlignment(Qt.AlignCenter)
    
    def show_empty_message(self):
        empty_label = QtWidgets.QLabel("No components added. Add components from the panel.")
        self.layout.addWidget(empty_label)
        # set central alignment
        self.layout.setAlignment(Qt.AlignCenter)
        

    def scrollbars(self, scrollbars: bool) -> None:
        if scrollbars:
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        

    def add_line(self):
        """
        Adds a horizontal line (or separator) to the layout.
        """
        line_height = max(1, int((self.height() * 0.3) // 150))  # Adjust the thickness of the line #TODO: Make dynamic
        line_width = int((self.width() * 0.1) // 3)  # One-third of the component width

        # Create a custom line using QLabel or QWidget
        line = QtWidgets.QWidget()
        line.setObjectName("NetworkConnectionLine")
        line.setFixedHeight(line_height)
        line.setFixedWidth(line_width)
        self.layout.addWidget(line)

    def resizeEvent(self, event):
        """
        Handle resize events to dynamically adjust component heights without flickering.
        """
        self.resize_timer.start(100)  # Trigger `handle_resize` after 100ms
        super().resizeEvent(event)
        
    def handle_resize(self):
        """
        Adjust component sizes after resizing is complete.
        """
        zoom = self.current_settings.get('zoom', 1)
        for i in range(self.layout.count()):
            child = self.layout.itemAt(i).widget()
            if child and isinstance(child, QtWidgets.QPushButton):  # Assuming your widgets are buttons
                scaling_factor = getattr(child, 'scaling_factor', 1)
                component_height = int(self.height() * 0.3 * scaling_factor * zoom)
                component_width = int(self.width() * 0.1 * scaling_factor * zoom)
                child.setFixedSize(component_width, component_height)
            # Adjust line width
            if child and child.objectName() == "NetworkConnectionLine":
                line_height = max(1, int((self.height() * 0.3) // 150))
                line_width = int((self.width() * 0.1) // 3)
                child.setFixedSize(line_width, line_height)

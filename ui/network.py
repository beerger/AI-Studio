from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QFrame, QHBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen
import pyqtgraph as pg
import numpy as np
from PyQt5.QtGui import QPixmap
from core.module import ModelManager
import torch

class Network(QtWidgets.QWidget):
    def __init__(self, model_manager, signal_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.signal_manager = signal_manager
        
        # Connect the signal manager's update_visualization_signal to the handle_component_list_update method
        self.signal_manager.update_visualization_signal.connect(self.handle_component_list_update)

        # Create a scroll area to wrap the layout
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a container widget for the layout
        self.container = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.container)
        self.layout.setSpacing(10)  # Adjust spacing between components
        self.layout.setAlignment(Qt.AlignLeft)  # Align components to the left
        self.scroll_area.setWidget(self.container)

        # Main layout to hold the scroll area
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        # Call render_network to initialize
        self.render_network()

    def render_network(self):
        """
        Renders the network based on the current model manager.
        Adds a line between each component.
        """
        # Clear the layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Calculate the fixed height for components (50% of the parent height)

        # Iterate through the components
        for i, component in enumerate(self.model_manager):
            # Add the component's widget
            widget = component.get_widget()
            component_height = int(self.height() * 0.3)
            component_width = int(self.width() * 0.1)
            if hasattr(widget, 'scaling_factor'):
                component_height = int(component_height * widget.scaling_factor)
            widget.setFixedSize(component_width, component_height)  # Fixed width and height (50% of screen height)
            current_stylesheet = widget.styleSheet()
            font_stylesheet = "font-size: 32px;"
            widget.setStyleSheet(current_stylesheet + font_stylesheet)  # Set the font size
            self.layout.addWidget(widget)

            # Add a line after each widget, except the last one
            if i < len(self.model_manager) - 1:
                self.add_line(component_width, component_height)

        # Add a spacer at the end to ensure proper alignment
        self.layout.addStretch()

    def add_line(self, component_width, component_height):
        """
        Adds a horizontal line (or separator) to the layout.
        """
        line_height = component_height // 150  # Adjust the thickness of the line
        line_width = component_width // 3  # One-third of the component width

        # Create a custom line using QLabel or QWidget
        line = QtWidgets.QWidget()
        line.setFixedHeight(line_height)
        line.setFixedWidth(line_width)
        line.setStyleSheet("background-color: black;")  # Set the color and thickness
        self.layout.addWidget(line)

    def resizeEvent(self, event):
        """
        Handle resize events to dynamically adjust component heights.
        """
        self.render_network()  # Re-render the network to update component sizes
        super().resizeEvent(event)

    def handle_component_list_update(self, model_manager):
        """
        Updates the model manager and refreshes the network display.
        """
        print("Network received updated component list.")
        self.model_manager = model_manager
        self.render_network()


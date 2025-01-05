from PyQt5 import QtWidgets, QtCore, QtGui
import re

class FrameLessPopup(QtWidgets.QDialog):
    def __init__(self, parent=None, vertical_layout=True):
        super(FrameLessPopup, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setObjectName("FramelessPopup")
        
        # Cache parsed style values
        self.border_thickness = 2  # Default value
        self.background_color = QtGui.QColor(40, 44, 52)  # Default background
        self.border_color = QtGui.QColor(44, 49, 58)  # Default border
        self.left_radius, self.right_radius = 10, 10  # Default radii
        
        # Main layout for the dialog
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(self.border_thickness, self.border_thickness, self.border_thickness, 10)

        # Custom title bar
        self.title_bar = QtWidgets.QWidget(self)
        #self.title_bar.setFixedHeight(30)
        self.title_bar.setObjectName("FramelessPopupTitleBar")
        #self.title_bar.setStyleSheet("border-top-left-radius: 10px; border-top-right-radius: 10px;")
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag
        self.title_bar.mouseReleaseEvent = self.stop_drag

        self.title_layout = QtWidgets.QHBoxLayout(self.title_bar)
        #self.title_layout.setContentsMargins(3, 0, 3, 20)

        # Title bar content
        self.title_label = QtWidgets.QLabel("Custom Dialog")
        self.title_label.setObjectName("FramelessPopupTitle")
        self.title_layout.addWidget(self.title_label, stretch=9)

        # Close button
        self.close_button = QtWidgets.QPushButton("X")
        # set background of button to same as title bar
        self.close_button.setObjectName("FramelessPopupCloseButton")
        self.close_button.clicked.connect(self.close)
        self.title_layout.addWidget(self.close_button, stretch=1)

        # Add title bar to the main layout
        self.main_layout.addWidget(self.title_bar, stretch=1)

        # Content area for subclasses
        self.content_area = QtWidgets.QWidget(self)

        # Add a layout to the content area
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area) if vertical_layout else QtWidgets.QHBoxLayout(self.content_area)
        #self.content_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed
        self.content_area.setLayout(self.content_layout)

        # Add the content area to the main layout
        self.main_layout.addWidget(self.content_area, stretch=9)

        # Enable dragging
        self.dragging = False
        
    def start_drag(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def perform_drag(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def stop_drag(self, event):
        self.dragging = False
        
    def parse_styles(self):
        # Parse the global stylesheet
        global_stylesheet = QtWidgets.QApplication.instance().styleSheet()
        self.left_radius, self.right_radius = self.extract_title_bar_radius(global_stylesheet)
        r, g, b = self.get_primary_background(global_stylesheet)
        self.background_color = QtGui.QColor(r, g, b)
        r, g, b = self.get_border(global_stylesheet)
        self.border_color = QtGui.QColor(r, g, b)
        print(self.left_radius, self.right_radius, self.background_color, self.border_color)
        
    def paintEvent(self, event):
        # Use cached style values for painting
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        rect.adjust(self.border_thickness // 2, self.border_thickness // 2,
                    -self.border_thickness // 2, -self.border_thickness // 2)

        # Draw the background
        painter.setBrush(self.background_color)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rect, self.left_radius, self.right_radius)

        # Draw the border
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(self.border_color, self.border_thickness))
        painter.drawRoundedRect(rect, self.left_radius, self.right_radius)

        
    def extract_title_bar_radius(self, qss_string):
        # Regex to match #FramelessPopupTitleBar block
        pattern = r"#FramelessPopupTitleBar\s*\{([^}]*)\}"
        match = re.search(pattern, qss_string, re.DOTALL)

        if match:
            block_content = match.group(1).strip()
            # Split the block content into individual style rules
            styles = dict(
                line.strip().split(":", 1) for line in block_content.split(";") if ":" in line
            )
        border_top_left_radius = styles.get("border-top-left-radius", 0)
        border_top_right_radius = styles.get("border-top-right-radius", 0)
        if border_top_left_radius != 0:
            border_top_left_radius = int(border_top_left_radius.replace("px", ""))
        if border_top_right_radius != 0:
            border_top_right_radius = int(border_top_right_radius.replace("px", ""))
        return border_top_left_radius, border_top_right_radius
    
    def get_primary_background(self, qss_string):
        pattern = r"QWidget\s*\{([^}]*)\}"
        match = re.search(pattern, qss_string, re.DOTALL)

        if match:
            block_content = match.group(1).strip()
            # Split the block content into individual style rules
            styles = dict(
                line.strip().split(":", 1) for line in block_content.split(";") if ":" in line
            )
        rgb = styles.get("background-color", 0)
        if rgb == 0:
            return 40, 44, 52
        # Check if its rgba
        if "rgba" in rgb:
            rgba = tuple(map(int, re.findall(r"\d+", rgb)))
            return self.convert_rgba_to_rgb(rgba)
        else:
            return tuple(map(int, re.findall(r"\d+", rgb)))

    def convert_rgba_to_rgb(self, rgba):
        # Convert an RGBA color to RGB
        r, g, b, a = rgba
        r = int((1 - a / 255) * 255 + a / 255 * r)
        g = int((1 - a / 255) * 255 + a / 255 * g)
        b = int((1 - a / 255) * 255 + a / 255 * b)
        return r, g, b

    def get_border(self, qss_string):
        pattern = r"#defaultBorder\s*\{([^}]*)\}"
        match = re.search(pattern, qss_string, re.DOTALL)

        if match:
            block_content = match.group(1).strip()
            # Split the block content into individual style rules
            styles = dict(
                line.strip().split(":", 1) for line in block_content.split(";") if ":" in line
            )
        rgb = styles.get("border", 0)
        if rgb == 0:
            return 40, 44, 52
        # Check if its rgba
        if "rgba" in rgb:
            rgba = tuple(map(int, re.findall(r"\d+", rgb)))
            return self.convert_rgba_to_rgb(rgba)
        else:
            return tuple(map(int, re.findall(r"\d+", rgb)))
        return tuple(map(int, re.findall(r"\d+", border)))
        
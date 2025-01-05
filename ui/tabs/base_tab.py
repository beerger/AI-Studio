from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import os
import constants.tabs as tabs_constants
from utils.file_helper import ICON_DIR
from PyQt5 import QtGui
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCursor

class BaseTab(QtWidgets.QWidget):
    def __init__(self, signal_manager, scaling_factor=1.0, category_dict=None, parent=None):
        super(BaseTab, self).__init__(parent)
        self.signal_manager = signal_manager
        self.scaling_factor = scaling_factor
        self.category_dict = category_dict or {}
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.action_widgets = []  # Track all action components
        self.icon_pixmaps = []  # Track pixmaps for scaling
        
        # Initialize the UI without scaling
        self.init_ui()
    
        # Calculate container dimensions based on current fonts and icons
        container_width, container_height = self.calculate_action_label_measures()
    
        # Apply scaling after determining accurate dimensions
        self.apply_scaling(self.scaling_factor, container_width, container_height)

    def init_ui(self):
        self.setup_actions(self.category_dict)
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(spacer)

    def setup_actions(self, category_dict):
        for category, actions in category_dict.items():
            v_layout = QtWidgets.QVBoxLayout()
            h_layout = QtWidgets.QHBoxLayout()

            for action in actions:
                # Create hoverable container
                container = QtWidgets.QFrame()
                container.setObjectName("hoverContainer")

                # Dynamically calculate container size
                container_width = tabs_constants.CONTAINER_WIDTH
                container_height = (
                    tabs_constants.ICON_SIZE
                    + tabs_constants.ACTION_FONT_SIZE * 2  # Approximate label height
                    + tabs_constants.CONTAINER_MARGIN_TOP
                    + tabs_constants.CONTAINER_MARGIN_BOTTOM
                )
                container.setFixedSize(container_width, container_height)

                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setContentsMargins(
                    tabs_constants.CONTAINER_MARGIN_LEFT,
                    tabs_constants.CONTAINER_MARGIN_TOP,
                    tabs_constants.CONTAINER_MARGIN_RIGHT,
                    tabs_constants.CONTAINER_MARGIN_BOTTOM,
                )
                container_layout.setSpacing(5)  # Adjust spacing between components if needed
                container_layout.setAlignment(QtCore.Qt.AlignTop)

                # Add the icon (GIF or PNG)
                icon_label = QtWidgets.QLabel()
                icon_label.setAlignment(QtCore.Qt.AlignCenter)
                icon_path = os.path.join(ICON_DIR, action['icon'])

                if action['icon'].lower().endswith('.gif'):
                    # Handle GIF
                    movie = QtGui.QMovie(icon_path)
                    #movie.setScaledSize(QtCore.QSize(tabs_constants.ICON_SIZE, tabs_constants.ICON_SIZE))
                    icon_label.setMovie(movie)
                    # set first frame as pixmap to display before animation starts
                    movie.jumpToFrame(0)
                    # start animation on hover
                    container.enterEvent = lambda event, movie=movie: movie.start()
                    # stop animation on leave and reset to first frame (do in a function to avoid lambda capture)
                    container.leaveEvent = lambda event, movie=movie: self.stop_movie(movie)
                    
                    self.icon_pixmaps.append((icon_label, movie))  # Track the movie object
                else:
                    # Handle PNG
                    pixmap = QtGui.QPixmap(icon_path)
                    pixmap_scaled = pixmap.scaled(
                        tabs_constants.ICON_SIZE,
                        tabs_constants.ICON_SIZE,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation,
                    )
                    icon_label.setPixmap(pixmap_scaled)
                    self.icon_pixmaps.append((icon_label, pixmap))

                container_layout.addWidget(icon_label)

                # Add the action label
                action_label = QtWidgets.QLabel(action['name'])
                action_label.setAlignment(QtCore.Qt.AlignCenter)
                action_label.setWordWrap(True)  # Enable word wrapping for longer titles
                container_layout.addWidget(action_label, QtCore.Qt.AlignBottom)

                # Connect action signals
                container.mousePressEvent = lambda event, sig=action['signal']: getattr(self.signal_manager, sig).emit()

                container.setCursor(QCursor(Qt.PointingHandCursor))

                h_layout.addWidget(container)
                self.action_widgets.append((container, icon_label, action_label))

            h_layout.setSpacing(tabs_constants.SPACING)
            v_layout.addLayout(h_layout)

            # Add category label
            category_label = QtWidgets.QLabel(category)
            category_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
            v_layout.addWidget(category_label)
            self.action_widgets.append((None, None, category_label))
            self.main_layout.addLayout(v_layout)

            # Add vertical line for separation
            vertical_line = QtWidgets.QFrame()
            vertical_line.setObjectName('categorySeparator')
            vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
            self.main_layout.addWidget(vertical_line)

    
    def stop_movie(self, movie):
        movie.stop()
        movie.jumpToFrame(0)

    def apply_scaling(self, scaling_factor, container_width=tabs_constants.CONTAINER_WIDTH, container_height=tabs_constants.CONTAINER_HEIGHT):
        self.scaling_factor = scaling_factor

        for container, icon_label, action_label in self.action_widgets:
            if container:
                container.setFixedSize(
                    int(container_width * self.scaling_factor),
                    int(container_height * self.scaling_factor)
                )

            #if icon_label:
            #    # Scale the icon
            #    original_pixmap = next((pix for label, pix in self.icon_pixmaps if label is icon_label), None)
            #    if original_pixmap:
            #        scaled_pixmap = original_pixmap.scaled(
            #            int(tabs_constants.ICON_SIZE * self.scaling_factor),
            #            int(tabs_constants.ICON_SIZE * self.scaling_factor),
            #            QtCore.Qt.KeepAspectRatio,
            #            QtCore.Qt.SmoothTransformation,
            #        )
            #        icon_label.setPixmap(scaled_pixmap)
            #
            if action_label:
                # Scale the font size of the label
                font = action_label.font()
                base_font_size = tabs_constants.ACTION_FONT_SIZE
                font.setPointSize(int(base_font_size * self.scaling_factor))
                action_label.setFont(font)



    def calculate_action_label_measures(self):
        """Calculate the required width and height for the largest action label and container."""
        max_width = 0
        max_height = 0

        for _, _, action_label in self.action_widgets:
            if action_label:  # Ensure it's a QLabel
                font_metrics = action_label.fontMetrics()

                # Calculate bounding rectangle with word wrapping
                container_width = tabs_constants.CONTAINER_WIDTH - (
                    tabs_constants.CONTAINER_MARGIN_LEFT + tabs_constants.CONTAINER_MARGIN_RIGHT
                )
                bounding_rect = font_metrics.boundingRect(
                    0, 0, container_width, 0, QtCore.Qt.TextWordWrap, action_label.text()
                )

                # Update maximum dimensions
                max_width = max(max_width, bounding_rect.width())
                max_height = max(max_height, bounding_rect.height())

        # Add icon height and margins
        max_height += tabs_constants.ICON_SIZE + tabs_constants.CONTAINER_MARGIN_TOP + tabs_constants.CONTAINER_MARGIN_BOTTOM
        max_width += tabs_constants.CONTAINER_MARGIN_LEFT + tabs_constants.CONTAINER_MARGIN_RIGHT

        # Apply scaling
        scaled_width = max_width * self.scaling_factor
        scaled_height = max_height * self.scaling_factor

        return scaled_width, scaled_height


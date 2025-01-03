from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import os
import constants.tabs as tabs_constants
from utils.file_helper import ICON_DIR

class BaseTab(QtWidgets.QWidget):
    def __init__(self, signal_manager, scaling_factor=1.0, category_dict=None, parent=None):
        super(BaseTab, self).__init__(parent)
        self.signal_manager = signal_manager
        self.scaling_factor = scaling_factor
        self.category_dict = category_dict or {}
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.action_widgets = []  # Track all action components
        self.icon_pixmaps = []  # Track pixmaps for scaling
        self.init_ui()
        self.apply_scaling(self.scaling_factor)

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
                container.setFixedSize(tabs_constants.CONTAINER_WIDTH, tabs_constants.CONTAINER_HEIGHT)

                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setContentsMargins(
                    tabs_constants.CONTAINER_MARGIN_LEFT,
                    tabs_constants.CONTAINER_MARGIN_TOP,
                    tabs_constants.CONTAINER_MARGIN_RIGHT,
                    tabs_constants.CONTAINER_MARGIN_BOTTOM
                )
                container_layout.setAlignment(QtCore.Qt.AlignTop)

                # Add the icon
                icon = QIcon(os.path.join(ICON_DIR, action['icon']))
                pixmap = icon.pixmap(tabs_constants.ORIGINAL_ICON_SIZE, tabs_constants.ORIGINAL_ICON_SIZE) 
                icon_label = QtWidgets.QLabel()
                icon_label.setPixmap(pixmap)
                icon_label.setAlignment(QtCore.Qt.AlignCenter)
                container_layout.addWidget(icon_label)
                self.icon_pixmaps.append((icon_label, pixmap))

                # Add the action label
                action_label = QtWidgets.QLabel(action['name'])
                action_label.setAlignment(QtCore.Qt.AlignCenter)
                action_label.setWordWrap(True)
                container_layout.addWidget(action_label, QtCore.Qt.AlignBottom)

                # Connect action signals
                container.mousePressEvent = lambda event, sig=action['signal']: getattr(self.signal_manager, sig).emit()

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
            vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
            vertical_line.setStyleSheet('color: lightGray')
            self.main_layout.addWidget(vertical_line)

    def apply_scaling(self, scaling_factor):
        print(f"Scaling {self.__class__.__name__}")
        self.scaling_factor = scaling_factor
        for container, icon_label, action_label in self.action_widgets:
            if container:
                container.setFixedSize(
                    int(tabs_constants.CONTAINER_WIDTH * self.scaling_factor),
                    int(tabs_constants.CONTAINER_HEIGHT * self.scaling_factor)
                )
            if icon_label:
                original_pixmap = next(pix for label, pix in self.icon_pixmaps if label is icon_label)
                scaled_pixmap = original_pixmap.scaled(
                    int(tabs_constants.ICON_SIZE * self.scaling_factor),
                    int(tabs_constants.ICON_SIZE * self.scaling_factor),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
            if action_label:
                font = action_label.font()
                # If container and icon label are none its a category label
                base_font_size = tabs_constants.CATEGORY_FONT_SIZE if (container is None and icon_label is None) else tabs_constants.ACTION_FONT_SIZE
                font.setPointSize(int(base_font_size * self.scaling_factor))
                action_label.setFont(font)

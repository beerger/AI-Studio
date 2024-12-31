from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from utils.file_helper import ICON_DIR
import os


tab_dictionary = {
    'Tools': [{'name': 'Validate Network', 'icon': 'validate_network.png', 'signal': 'validate_network_signal'},
              {'name': 'Generate Summary', 'icon': 'generate_summary.png', 'signal': 'generate_summary_signal'},
              {'name': 'Import Model', 'icon': 'import_pretrained.png', 'signal': 'import_pretrained_signal'},
              {'name': 'Export to ONNX', 'icon': 'export_onnx.png', 'signal': 'export_onnx_signal'},
              {'name': 'Generate code', 'icon': 'generate_code.png', 'signal': 'generate_code_signal'},
              ],
}

class ToolsTab(QtWidgets.QWidget):
    
    def __init__(self, signal_manger, parent=None):
        super(ToolsTab, self).__init__(parent)
        self.signal_manager = signal_manger
        self.init_ui()
        
    def init_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        
        self.setup_actions(tab_dictionary)
        
        horizontal_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(horizontal_spacer)
        
    def setup_actions(self, category_dict):

        for category, value in category_dict.items():
            v_layout = QtWidgets.QVBoxLayout()
            h_layout = QtWidgets.QHBoxLayout()
            for action in value:
                # Create a QFrame to act as the hoverable container
                container = QtWidgets.QFrame()
                container.setObjectName("hoverContainer")  # Set an object name for styling
                container.setFixedSize(96, 96)  # Adjust size

                # Add a layout to the container
                container_layout = QtWidgets.QVBoxLayout(container)
                container_layout.setContentsMargins(5, 5, 5, 5)
                container_layout.setAlignment(QtCore.Qt.AlignCenter)

                # Add the icon
                icon = QIcon(os.path.join(ICON_DIR, action['icon']))
                icon_label = QtWidgets.QLabel()
                icon_label.setPixmap(icon.pixmap(48, 48))  # Set icon size
                icon_label.setAlignment(QtCore.Qt.AlignCenter)
                container_layout.addWidget(icon_label)

                # Add the action label
                action_label = QtWidgets.QLabel(action['name'])
                action_label.setAlignment(QtCore.Qt.AlignCenter)
                action_label.setWordWrap(True)  # Allow text wrapping
                container_layout.addWidget(action_label)

                # Apply hover effect to the QFrame only
                container.setStyleSheet("""
                    QFrame#hoverContainer {
                        border: none;
                        background-color: transparent;
                    }
                    QFrame#hoverContainer:hover {
                        border: 2px solid lightGray;
                        border-radius: 4px;
                    }
                """)

                # Connect mouse press event
                container.mousePressEvent = lambda event, sig=action['signal']: getattr(self.signal_manager, sig).emit()

                # Add container to the horizontal layout
                h_layout.addWidget(container)
    
            #
            h_layout.setSpacing(10)

            # Add the horizontal layout to the vertical layout
            v_layout.addLayout(h_layout)

            # Add the category label below the buttons
            label = QtWidgets.QLabel(category)
            label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
            v_layout.addWidget(label)

            # Add the completed vertical layout to the main layout
            self.main_layout.addLayout(v_layout)

            # Add a vertical line for separation
            vertical_line = QtWidgets.QFrame()
            vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
            vertical_line.setStyleSheet('color: lightGray')
            self.main_layout.addWidget(vertical_line)   
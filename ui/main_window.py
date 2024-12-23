from PyQt5 import QtCore, QtWidgets, QtGui
import torch.nn as nn
from ui.add_component_popup import AddComponentPopup
from ui.component_layout import ComponentLayoutWidget
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(QtCore.QRect(0, 0, 2000, 600))
        MainWindow.showMaximized()

        # Change icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/OneDrive - Uppsala universitet/General/AI-Studio/assets/company_logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        horizontal_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        horizontal_layout.addWidget(ComponentLayoutWidget())
        
        label_image = QtWidgets.QLabel(self.centralwidget)
        label_image.setPixmap(QtGui.QPixmap("D:/OneDrive - Uppsala universitet/General/AI-Studio/assets/company_logo.png"))
        horizontal_layout.addWidget(label_image, stretch=10)

        vertical_layout = QtWidgets.QVBoxLayout()
        # Popup button
        self.buttonPopup = QtWidgets.QPushButton(self.centralwidget)
        self.buttonPopup.clicked.connect(self.open_add_component_popup)
        self.buttonPopup.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        vertical_layout.addWidget(self.buttonPopup, stretch=2)

        # TODO: Remove this test button
        self.buttonTest = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTest.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        vertical_layout.addWidget(self.buttonTest, stretch=1)
        
        horizontal_layout.addLayout(vertical_layout)
        

        # Menu
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.popup = None  # Track the popup instance

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_add_component_popup(self):
        if self.popup is None or not self.popup.isVisible():
            self.popup = AddComponentPopup(component_type='activations', component_name="LeakyReLU", parent=self.centralwidget)
            self.popup.show()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("AI Studio", "AI Studio"))
        self.buttonPopup.setText(_translate("MainWindow", "Popup"))




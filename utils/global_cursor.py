from PyQt5 import QtCore, QtWidgets, QtGui

class GlobalCursorSetter(QtCore.QObject):
    def eventFilter(self, obj, event):
        # Check for QPushButton widgets
        if isinstance(obj, QtWidgets.QPushButton):
            # Apply the cursor for QPushButton when it is shown
            if event.type() == QtCore.QEvent.Show:
                obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Return the default event handling
        return super(GlobalCursorSetter, self).eventFilter(obj, event)

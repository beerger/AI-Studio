from utils.global_cursor import GlobalCursorSetter

if __name__ == "__main__":
    import sys
    from PyQt5.QtGui import QGuiApplication
    from ui.main_window import Ui_MainWindow
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt
    from core.signal_manager import SignalManager
    from PyQt5 import QtGui

    # Enable high DPI scaling
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Create the application
    app = QtWidgets.QApplication(sys.argv)
    cursor_pixmap = QtGui.QPixmap("D:/OneDrive - Uppsala universitet/General/AI-Studio/resources/icons/cursor_3d_2.png")
    scaled_cursor_pixmap = cursor_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    custom_cursor = QtGui.QCursor(scaled_cursor_pixmap, 0, 0)  # Hotspot at top-left corner
    app.setOverrideCursor(custom_cursor)
    
    # Install the global event filter
    # This will set the cursor to a pointing hand for all buttons
    global_cursor_setter = GlobalCursorSetter()
    app.installEventFilter(global_cursor_setter)

    # Signal manager
    signal_manager = SignalManager()
    
    def calculate_scaling_factor(screen):
        """
        Calculate the scaling factor based on the DPI and resolution of the screen.
        """
        if not screen:
            print("No active screen detected. Default scaling factor used.")
            return 1.0

        current_dpi = screen.physicalDotsPerInch()
        baseline_dpi = 80
        logical_resolution = screen.size()
        device_pixel_ratio = screen.devicePixelRatio()
        physical_resolution = logical_resolution * device_pixel_ratio

        #print(f"Screen: {screen.name()}")
        #print(f"Logical Resolution: {logical_resolution}")
        #print(f"Device Pixel Ratio: {device_pixel_ratio}")
        #print(f"Physical Resolution: {physical_resolution}")

        baseline_resolution = (3840, 2160)
        dpi_scaling = current_dpi / baseline_dpi
        resolution_scaling = max(1.0, min(
            physical_resolution.width() / baseline_resolution[0],
            physical_resolution.height() / baseline_resolution[1]
        ))
        scaling_factor = dpi_scaling * resolution_scaling

        #print(f"Calculated Scaling Factor: {scaling_factor}")
        return scaling_factor

    initial_screen = QGuiApplication.primaryScreen()
    scaling_factor = calculate_scaling_factor(initial_screen)

    def handle_window_screen_change(new_screen):
        if new_screen:
            print(f"Window moved to screen: {new_screen.name()}")
            new_scaling_factor = calculate_scaling_factor(new_screen)
            print(f"New Scaling Factor: {new_scaling_factor}")
            signal_manager.apply_scaling.emit(new_scaling_factor)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(scaling_factor=scaling_factor, signal_manager=signal_manager)

    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # Connect screenChanged signal to detect when the window changes screens
    window_handle = MainWindow.windowHandle()
    if window_handle:
        window_handle.screenChanged.connect(handle_window_screen_change)
    else:
        print("Warning: No window handle available for screenChanged connection.")

    sys.exit(app.exec_())


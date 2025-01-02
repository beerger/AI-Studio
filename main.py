if __name__ == "__main__":
    import sys
    from PyQt5.QtGui import QGuiApplication
    from ui.main_window import Ui_MainWindow
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt
    from core.signal_manager import SignalManager

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QtWidgets.QApplication(sys.argv)
    signal_manager = SignalManager()

    def calculate_scaling_factor(screen):
        if not screen:
            print("No active screen detected. Default scaling factor used.")
            return 1.0

        current_dpi = screen.physicalDotsPerInch()
        baseline_dpi = 80
        logical_resolution = screen.size()
        device_pixel_ratio = screen.devicePixelRatio()
        physical_resolution = logical_resolution * device_pixel_ratio

        print(f"Screen: {screen.name()}")
        print(f"Logical Resolution: {logical_resolution}")
        print(f"Device Pixel Ratio: {device_pixel_ratio}")
        print(f"Physical Resolution: {physical_resolution}")

        baseline_resolution = (3840, 2160)
        dpi_scaling = current_dpi / baseline_dpi
        resolution_scaling = max(1.0, min(
            physical_resolution.width() / baseline_resolution[0],
            physical_resolution.height() / baseline_resolution[1]
        ))
        scaling_factor = dpi_scaling * resolution_scaling

        print(f"Calculated Scaling Factor: {scaling_factor}")
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

    sys.exit(app.exec_())

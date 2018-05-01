import sys

from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        desktop = QtWidgets.QDesktopWidget()
        help(desktop)
        print(desktop)
        geometry = desktop.availableGeometry()
        help(geometry)
        print(geometry)
        self.setGeometry(geometry)

    pass


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec_())

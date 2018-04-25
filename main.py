import sys

from PyQt5 import QtWidgets

import shared_data
# Menu
from widgets.widgets import AddWalletWidget, DeleteWalletWidget
# Widgets
from widgets.widgets import InfoWidget, WalletWidget, AddOrder, DeleteOrder


class MainWindow(QtWidgets.QMainWindow):
    WIDTH = 1200
    HEIGHT = 900

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_order_action = QtWidgets.QAction('Add Order', self)
        self.cancel_order_action = QtWidgets.QAction('Cancel Order', self)
        self.set_general_options()
        self.set_widgets()
        self.set_menu()

    def set_general_options(self):  # general options for the window

        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle('Trader')
        center(self)

    def set_menu(self):
        """Menu constructor
        """
        # File
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        # Wallet
        add_wallet_action = QtWidgets.QAction('Add Wallet', self)
        add_wallet_action.triggered.connect(self.add_wallet_widget.show)
        delete_wallet_action = QtWidgets.QAction('Delete Wallet', self)
        delete_wallet_action.triggered.connect(self.delete_wallet_widget.show)
        # Orders
        self.add_order_action.triggered.connect(self.add_order.show)
        self.cancel_order_action.triggered.connect(self.delete_order.show)
        # Menu:
        menu = self.menuBar()
        # File
        menu_element = menu.addMenu('&File')
        menu_element.addAction(exit_action)
        # Wallet
        wallet_menu = menu.addMenu('&Wallet')
        wallet_menu.addAction(add_wallet_action)
        wallet_menu.addAction(delete_wallet_action)
        # Orders
        orders_menu = menu.addMenu('&Orders')
        orders_menu.addAction(self.add_order_action)
        orders_menu.addAction(self.cancel_order_action)

    def set_widgets(self):
        self.info_widget = InfoWidget(parent=self)
        self.wallet_widget = WalletWidget(parent=self)
        self.add_wallet_widget = AddWalletWidget()
        self.delete_wallet_widget = DeleteWalletWidget()
        self.add_order = AddOrder()
        self.delete_order = DeleteOrder()


if __name__ == '__main__':
    shared_data.dataUpdater.start()
    trader_app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(trader_app.exec_())

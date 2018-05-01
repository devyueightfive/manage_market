from PyQt5 import QtWidgets, QtCore

import sharedData
from gui.widgets.BasicWidgets import Bar
from gui.widgets.walletinformation.Tables import BalanceTable, OrdersTable
from wallet.wallets import Wallets


class WalletInformation(QtWidgets.QWidget):

    def __init__(self, x, y, width, height, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.box = QtWidgets.QGroupBox('Wallet', self)
        self.wallet_bar = Bar('Wallet', sharedData.names_of_wallets, 20, 30, 70, 30, self.box)
        self.balance_table = BalanceTable(self.box)
        self.order_table = OrdersTable(self.box)
        self.setGeometryForWidget()
        self.setSlots()

    def setGeometryForWidget(self):
        print("WidgetForWalletInformation: ", (self.x, self.y, self.width, self.height))
        geometry = QtCore.QRect(self.x,
                                self.y,
                                self.width,
                                self.height)
        self.setGeometry(geometry)

        geometry = QtCore.QRect(self.parent().shiftFromBorder,
                                self.parent().shiftFromBorder,
                                self.width - 2 * self.parent().shiftFromBorder,
                                self.height - 2 * self.parent().shiftFromBorder)
        self.box.setGeometry(geometry)

        self.balance_table.setGeometry(QtCore.QRect(2, 100, 160, 315))
        self.order_table.setGeometry(QtCore.QRect(180, 15, 540, 400))

    def setSlots(self):
        self.wallet_bar.combo.currentTextChanged.connect(self.select_wallet)
        sharedData.walletBalance.changed.connect(self.balance_table.updateBalance)
        sharedData.walletBalance.changed.connect(self.order_table.updateOrders)

    def select_wallet(self):
        sharedData.walletNameSelectedByUser = self.wallet_bar.combo.currentText()
        if sharedData.walletNameSelectedByUser != '':
            sharedData.lastRequestTimeForTradeAPI = 0
            sharedData.walletSelectedByUser.clear()
            sharedData.walletSelectedByUser.update(
                Wallets.getWallet(sharedData.walletNameSelectedByUser).Value)

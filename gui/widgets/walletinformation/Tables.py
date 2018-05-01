from time import ctime

from PyQt5 import QtWidgets, QtGui, QtCore

from gui.wallet_model import OrderModel, BalanceModel
from sharedData import walletBalance as shared_balance


class OrdersTable(QtWidgets.QTableWidget):
    ROWS = 0
    COLUMNS = len(OrderModel.attributes)

    def __init__(self, *args):
        super().__init__(*args)
        self.setColumnCount(self.COLUMNS)
        self.setRowCount(self.ROWS)
        self.setHorizontalHeaderLabels(OrderModel.attributes)
        self.horizontalHeader().setStyleSheet("color: blue")
        # self.setSizeAdjustPolicy(QtWidgets.QTableWidget.AdjustToContents)
        for l in range(len(OrderModel.attribute_length)):
            self.setColumnWidth(l, OrderModel.attribute_length[l])

        self.setupContextMenu()

    def __fillRow(self, order: dict, row: int):
        for index in range(len(OrderModel.attributes)):
            attribute = OrderModel.attributes[index]
            value = order.get(attribute, '')
            if attribute == 'timestamp_created':
                value = ctime(float(value))
            item = QtWidgets.QTableWidgetItem(str(value))
            brush = QtGui.QBrush()
            if order.get('type') == 'buy':
                brush.setColor(QtCore.Qt.darkGreen)
            else:
                brush.setColor(QtCore.Qt.red)
            item.setForeground(brush)
            self.setItem(row, index, item)

    def __updateView(self, orders: dict):
        self.clearSpans()
        self.ROWS = len(orders)
        self.setRowCount(self.ROWS)
        row = 0
        for k, v in orders.items():
            v['id'] = k
            self.__fillRow(v, row)
            row += 1

    def updateOrders(self):
        self.__updateView(shared_balance.value.get('orders', {}))

    def setupContextMenu(self):
        wallet_widget = self.parent()
        main_window = wallet_widget.parent().parent()
        self.addAction(main_window.actionOrderCreation)
        self.addAction(main_window.actionOrderCancellation)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)


class BalanceTable(QtWidgets.QTableWidget):
    ROWS = 0
    COLUMNS = len(BalanceModel.attributes)

    def __init__(self, *args):
        super().__init__(*args)
        self.setColumnCount(self.COLUMNS)
        self.setRowCount(self.ROWS)
        self.setHorizontalHeaderLabels(BalanceModel.attributes)
        self.horizontalHeader().setStyleSheet("color: blue")

        for l in range(len(BalanceModel.attribute_length)):
            self.setColumnWidth(l, BalanceModel.attribute_length[l])

    def __updateView(self, balance: dict):
        self.clearSpans()
        self.ROWS = len(balance)
        self.setRowCount(self.ROWS)
        row = 0
        for key, value in balance.items():
            self.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            self.setItem(row, 1, QtWidgets.QTableWidgetItem('{:0,.8f}'.format(float(value))))
            row += 1

    def updateBalance(self):
        self.__updateView(shared_balance.value.get('funds', {}))

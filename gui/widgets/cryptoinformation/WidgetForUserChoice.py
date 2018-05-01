from PyQt5 import QtWidgets, QtCore

import sharedData
from gui.widgets.BasicWidgets import Bar


class UserChoice(QtWidgets.QWidget):

    def __init__(self, x, y, width, height, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.setGeometryForWidget()
        self.comboBoxForTradePair = Bar('Pair', sharedData.supportedTradePairs, 10, 55, 95, 50, self)
        self.comboBoxForWalletName = Bar('Market', sharedData.supportedMarkets, 10, 25, 95, 20, self)
        self.set_slots()

    def setGeometryForWidget(self):
        print("UserChoice: ", (self.x, self.y, self.width, self.height))
        geometry = QtCore.QRect(self.x,
                                self.y,
                                self.width,
                                self.height)
        self.setGeometry(geometry)

    def set_slots(self):
        self.comboBoxForWalletName.combo.currentTextChanged.connect(self.select_public_market)
        self.comboBoxForTradePair.combo.currentTextChanged.connect(self.select_public_symbol)
        sharedData.tradePairTicker.changed.connect(self.parent().parent().tickerOfCryptoCoin.update_info)

    def select_public_market(self):
        sharedData.marketURLSelectedByUser = self.comboBoxForWalletName.combo.currentText()
        sharedData.lastRequestTimeForPublicAPI = 0

    def select_public_symbol(self):
        sharedData.tradePairSelectedByUser = self.comboBoxForTradePair.combo.currentText()
        sharedData.lastRequestTimeForPublicAPI = 0

import re

from PyQt5 import QtWidgets, QtCore
from bs4 import BeautifulSoup

import sharedData
from gui.widgets.BasicWidgets import TextLine, Bar
from marketAPI import getApi
from wallet.wallets import Wallets


class AddWalletWidget(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()

    def set_general_options(self):  # general options for the window
        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(530, 200)
        self.setWindowTitle('Add Wallet ...')
        center()

    def set_widgets(self):
        wallet_text_bar = TextLine('Wallet name :', '', 20, 30, 120, 30, self, text_width=130)
        market_text_bar = TextLine('Market address :', '', 280, 30, 380, 30, self, text_width=130)
        key_text_bar = TextLine('Key :', '', 20, 70, 120, 70, self, text_width=390)
        sign_text_bar = TextLine('Sign :', '', 20, 110, 120, 110, self, text_width=390)
        save_button = QtWidgets.QPushButton('Save', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 150)

        # actions
        def on_push_save():
            wallet_to_save = {'name': wallet_text_bar.text_edit.text(),
                              'market': market_text_bar.text_edit.text(),
                              'key': key_text_bar.text_edit.text(),
                              'sign': sign_text_bar.text_edit.text(),
                              'robots': {}}
            Wallets.add(wallet_to_save)
            # global wallet_names
            sharedData.names_of_wallets.clear()
            sharedData.names_of_wallets.extend(Wallets.getListOfWallets().Value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_save)


class DeleteWalletWidget(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()

    def set_general_options(self):  # general options for the window

        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(250, 120)
        self.setWindowTitle('Delete Wallet ...')
        center()

    def set_widgets(self):
        # global wallet_names
        wallet_bar = Bar('Wallet name :', sharedData.names_of_wallets, 20, 30, 120, 30, self)
        save_button = QtWidgets.QPushButton('Delete', self)
        save_button_width = save_button.width()
        save_button.move(int((self.width() - save_button_width) / 2), 70)

        # actions
        def on_push_delete():
            Wallets.deleteWallet(wallet_bar.combo.currentText())
            sharedData.names_of_wallets.clear()
            sharedData.names_of_wallets.extend(Wallets.getListOfWallets().Value)
            self.close()

        # bind actions with button
        save_button.clicked.connect(on_push_delete)


class AddOrder(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()
        self.set_slots()

    def set_general_options(self):  # general options for the window
        self.resize(440, 190)
        self.setWindowTitle('Add Order ...')
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getCurrencyBalance(self):
        # should be defined shared.balance
        if sharedData.walletNameSelectedByUser not in ['', None]:
            pair = self.pairText.combo.currentText()
            actionType = self.typeBar.combo.currentText()
            print(f"Pair = {pair}")
            if pair not in ['', None] and actionType not in ['', None]:
                coin, currency = pair.split('_')
                if self.typeBar.combo.currentText() == 'buy':
                    remains = sharedData.walletBalance.value.get('funds').get(currency, 0)
                else:
                    remains = sharedData.walletBalance.value.get('funds').get(coin, 0)
                return self.currencyBalance.setText(
                    '<center><u style="color:#0000ff;">{:0,.8f}</u></center>'.format(
                        remains)
                )
            return self.currencyBalance.setText("")

    def set_widgets(self):
        self.typeBar = Bar("Type:", ['sell', 'buy'], 20, 20, 70, 20, self)
        self.pairText = Bar("Pair:", sharedData.supportedTradePairs, 220, 20, 270, 20, self)
        label = QtWidgets.QLabel(self)
        label.setText("On Balance:")
        label.move(200, 60)
        self.currencyBalance = QtWidgets.QLabel(self)
        self.currencyBalance.setTextFormat(QtCore.Qt.RichText)
        self.currencyBalance.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.currencyBalance.resize(100, 15)
        self.currencyBalance.move(270, 60)
        self.rateText = TextLine("Rate:", '', 20, 100, 70, 100, self)
        self.amountText = TextLine("Amount:", '', 220, 100, 270, 100, self)

        self.create_button = QtWidgets.QPushButton('Add Order', self)
        self.create_button_width = self.create_button.width()
        self.create_button.move(int((self.width() - self.create_button_width) / 2), 150)

    def set_slots(self):
        self.create_button.clicked.connect(self.__action_AddOrder)
        self.pairText.combo.currentTextChanged.connect(self.getCurrencyBalance)
        self.typeBar.combo.currentTextChanged.connect(self.getCurrencyBalance)

    def mousePressEvent(self, event):
        self.fillAmount()

    def fillAmount(self):
        typeAction = self.typeBar.combo.currentText()
        rate = self.rateText.text_edit.text()
        remains = self.currencyBalance.text()
        remains = BeautifulSoup(remains, "html.parser").text
        if re.match("^\d+?\.?\d+?$", rate) and re.match("^\d+?\.?\d+?$", remains):
            amount = 0
            if typeAction == 'buy':
                marketApi = getApi(sharedData.walletSelectedByUser.get('market'))[0]
                amount = float(remains) / float(rate) * (1 - marketApi.marketFine)
            elif typeAction == 'sell':
                amount = float(remains)
            self.amountText.text_edit.setText(str(int(amount * 10 ** 8) / 10 ** 8))
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Some error")
            mb.setWindowTitle("Error")
            mb.exec()

    def __action_AddOrder(self):
        actionType = self.typeBar.combo.currentText()
        pair = self.pairText.combo.currentText()
        rate = self.rateText.text_edit.text()
        amount = self.amountText.text_edit.text()
        if actionType not in ['', None] and pair not in ['', None]:
            if re.match("^\d+?\.?\d+?$", rate) and re.match("^\d+?\.?\d+?$", amount):
                wallet = sharedData.walletSelectedByUser
                api = getApi(sharedData.walletSelectedByUser.get('market'))[0]
                response = api.requestOrderCreation(pair, actionType, float(rate), float(amount), wallet)
                sharedData.lastRequestTimeForTradeAPI = 0
                self.close()
                if response['success'] == 0:
                    mb = QtWidgets.QMessageBox()
                    mb.setText(response.get('error', 'Error'))
                    mb.setWindowTitle("Error")
                    mb.exec()
            else:
                mb = QtWidgets.QMessageBox()
                mb.setText("Please select rate/amount.")
                mb.setWindowTitle("Warning")
                mb.exec()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select type/pair.")
            mb.setWindowTitle("Warning")
            mb.exec()

    def show(self):
        if sharedData.walletNameSelectedByUser not in ['', None]:
            super().show()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select a wallet.")
            mb.setWindowTitle("Warning")
            mb.exec()


class DeleteOrder(QtWidgets.QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.orderNumbers = []
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_widgets()

    def set_general_options(self):  # general options for the window

        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(440, 120)
        self.setWindowTitle('Cancel Order ...')
        center()

    def set_widgets(self):
        print("Set Up")
        delete_button = QtWidgets.QPushButton('Cancel Order', self)
        delete_button_width = delete_button.width()
        delete_button.move(int((self.width() - delete_button_width) / 2), 60)
        self.orderID = Bar("Order id:", self.orderNumbers,
                           100, 20, 200, 20, self, combo_width=150)
        delete_button.clicked.connect(self.__action_DeleteOrder)

    def show(self):
        if sharedData.walletNameSelectedByUser not in ['', None]:
            super().show()
            self.orderNumbers.clear()
            self.orderNumbers.extend(
                list(sharedData.walletBalance.value.get('orders', {}).keys()))
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select a wallet.")
            mb.setWindowTitle("Warning")
            mb.exec()

    def __action_DeleteOrder(self):
        order_id = self.orderID.combo.currentText()
        if order_id not in ['', None]:
            wallet = sharedData.walletSelectedByUser
            api = getApi(sharedData.walletSelectedByUser.get('market'))[0]
            response = api.requestOrderCancellation(self.orderID.combo.currentText(), wallet)
            sharedData.lastRequestTimeForTradeAPI = 0
            if response['success'] == 0:
                mb = QtWidgets.QMessageBox()
                mb.setText(response.get('error', 'Error'))
                mb.setWindowTitle("Error")
                mb.exec()
            self.close()
        else:
            mb = QtWidgets.QMessageBox()
            mb.setText("Please select Order ID")
            mb.setWindowTitle("Warning")
            mb.exec()

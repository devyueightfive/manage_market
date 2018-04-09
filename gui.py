import sys
import time

from PyQt5 import QtCore, QtWidgets, QtChart

import settings
from wallets2 import Wallets
from widgets import AddWalletWidget, DeleteWalletWidget, Bar, PublicChart


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_wallet_widget = AddWalletWidget()
        self.delete_wallet_widget = DeleteWalletWidget()
        self.init_ui()

    def init_ui(self):
        self.set_general_options()
        self.set_menu()
        self.set_widgets()
        self.bind_global_parameters_with_actions()

    def set_general_options(self):  # general options for the window
        def center(w=self):
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr = w.frameGeometry()
            qr.moveCenter(cp)
            w.move(qr.topLeft())

        self.resize(800, 900)
        self.setWindowTitle('Trader')
        center()

    def set_menu(self):
        # actions
        # ~for manipulating with a wallet
        add_wallet_action = QtWidgets.QAction(text='Add Wallet', parent=self)
        add_wallet_action.triggered.connect(self.add_wallet_widget.show)
        delete_wallet_action = QtWidgets.QAction(text='Delete Wallet', parent=self)
        delete_wallet_action.triggered.connect(self.delete_wallet_widget.show)
        # menu constructing
        menu = self.menuBar()
        wallet_menu = menu.addMenu('&Wallet')
        wallet_menu.addAction(add_wallet_action)
        wallet_menu.addAction(delete_wallet_action)

    def set_widgets(self):
        #
        # public_box
        self.public_info_box = QtWidgets.QGroupBox('Public Info', self)
        self.public_info_box.setGeometry(QtCore.QRect(10, 40, 780, 390))
        self.public_pair = Bar('Pair', settings.supported_pairs, 20, 20, 70, 20, True, self.public_info_box)
        self.public_market = Bar('Market', settings.supported_markets, 20, 50, 70, 50, True, self.public_info_box)
        #
        # pair_info_box
        self.pair_info_box = QtWidgets.QGroupBox('Pair Info', self.public_info_box)
        self.pair_info_box.setGeometry(QtCore.QRect(180, 10, 590, self.public_info_box.geometry().height() - 20))
        #
        p_label = QtWidgets.QLabel('Last:', self.pair_info_box)
        p_label.setGeometry(10, 20, 60, 20)
        self.p_last = QtWidgets.QLabel('last_info', self.pair_info_box)
        self.p_last.setGeometry(40, 20, 70, 20)
        #
        p_label = QtWidgets.QLabel('Avg:', self.pair_info_box)
        p_label.setGeometry(10, 40, 60, 20)
        self.p_avg = QtWidgets.QLabel('avg_info', self.pair_info_box)
        self.p_avg.setGeometry(40, 40, 70, 20)
        #
        p_label = QtWidgets.QLabel('Sell:', self.pair_info_box)
        p_label.setGeometry(130, 20, 30, 20)
        self.p_sell_price = QtWidgets.QLabel('sell_info', self.pair_info_box)
        self.p_sell_price.setGeometry(160, 20, 70, 20)
        #
        p_label = QtWidgets.QLabel('Buy:', self.pair_info_box)
        p_label.setGeometry(130, 40, 30, 20)
        self.p_buy_price = QtWidgets.QLabel('buy_info', self.pair_info_box)
        self.p_buy_price.setGeometry(160, 40, 70, 20)
        #
        p_label = QtWidgets.QLabel('High:', self.pair_info_box)
        p_label.setGeometry(250, 20, 30, 20)
        self.p_high = QtWidgets.QLabel('high_info', self.pair_info_box)
        self.p_high.setGeometry(280, 20, 70, 20)
        #
        p_label = QtWidgets.QLabel('Low:', self.pair_info_box)
        p_label.setGeometry(250, 40, 30, 20)
        self.p_low = QtWidgets.QLabel('low_info', self.pair_info_box)
        self.p_low.setGeometry(280, 40, 70, 20)
        #
        # plot
        public_plot = PublicChart()
        cv = QtChart.QChartView()
        cv.setChart(public_plot)
        cv.setParent(self.pair_info_box)
        cv.setGeometry(5, 60, self.pair_info_box.geometry().width() - 10,
                       self.pair_info_box.geometry().height() - 65)
        cv.setRenderHint(True)

        # wallet_box
        self.wallet_box = QtWidgets.QGroupBox('Wallet', self)
        self.wallet_box.setGeometry(QtCore.QRect(10, self.public_info_box.geometry().bottom() + 10, 780, 250))
        self.wallet_bar = Bar('Wallet', settings.names_of_wallets, 20, 30, 70, 30, True, self.wallet_box)
        #
        self.sell_orders_box = QtWidgets.QGroupBox(self.wallet_box)
        self.sell_orders_box.setGeometry(QtCore.QRect(180, 10, 200, self.wallet_box.geometry().height() - 20))
        self.sell_orders_box.setTitle("Sell Orders")
        #
        self.sell_orders_textBrowser = QtWidgets.QTextBrowser(self.sell_orders_box)
        self.sell_orders_textBrowser.setGeometry(QtCore.QRect(5, 20,
                                                              self.sell_orders_box.geometry().width() - 10, 205))
        #
        self.buy_orders_box = QtWidgets.QGroupBox(self.wallet_box)
        self.buy_orders_box.setGeometry(QtCore.QRect(400, 10, 200, self.wallet_box.geometry().height() - 20))
        self.buy_orders_box.setTitle("Buy Orders")
        #
        self.buy_orders_textBrowser = QtWidgets.QTextBrowser(self.buy_orders_box)
        self.buy_orders_textBrowser.setGeometry(QtCore.QRect(5, 20,
                                                             self.buy_orders_box.geometry().width() - 10, 205))
        #
        self.balance_box = QtWidgets.QGroupBox(self.wallet_box)
        self.balance_box.setGeometry(QtCore.QRect(620, 10, 150, self.wallet_box.geometry().height() - 20))
        self.balance_box.setTitle("Balance")
        #
        self.balance_box_textBrowser = QtWidgets.QTextBrowser(self.balance_box)
        self.balance_box_textBrowser.setGeometry(QtCore.QRect(5, 20, 140, 205))
        #
        # robot_box
        robot_box = QtWidgets.QGroupBox('Robot', self)
        robot_box.setGeometry(QtCore.QRect(10, self.wallet_box.geometry().bottom() + 10, 780, 200))
        self.robot_bar = Bar('Robot', settings.robot_names, 20, 30, 70, 30, False, robot_box)

        #

        # actions to selections from combo boxes

        def on_change_wallet_bar():
            settings.selected_wallet_name = self.wallet_bar.combo.currentText()
            if settings.selected_wallet_name != '':
                settings.selected_wallet.update(
                    Wallets.get_wallet_by_name(settings.selected_wallet_name).value)
                settings.robot_names.clear()
                settings.robot_names.extend(
                    Wallets.get_list_of_robot_names_by_wallet_name(settings.selected_wallet_name).value)
                self.robot_bar.combo.setCurrentIndex(-1)
                self.robot_bar.set_enabled(True) if len(settings.robot_names) else self.robot_bar.set_enabled(False)

        def on_change_market_bar():
            settings.selected_public_market = self.public_market.combo.currentText()

        def on_change_pair_bar():
            settings.selected_public_pair = self.public_pair.combo.currentText()

        self.wallet_bar.combo.currentTextChanged.connect(on_change_wallet_bar)
        self.public_market.combo.currentTextChanged.connect(on_change_market_bar)
        self.public_pair.combo.currentTextChanged.connect(on_change_pair_bar)

    def bind_global_parameters_with_actions(self):
        # actions on responses from WebAPI requests
        def on_public_pair_change():
            # print(settings.public_pair_value.value)
            if len(settings.public_pair_value.value.keys()) > 0:
                self.p_sell_price.setText(str(settings.public_pair_value.value.get('sell', 'sell_info')))
                self.p_buy_price.setText(str(settings.public_pair_value.value.get('buy', 'buy_info')))
                self.p_last.setText(str(settings.public_pair_value.value.get('last', 'last_info')))
                self.p_avg.setText(str(settings.public_pair_value.value.get('avg', 'avg_info')))
                self.p_high.setText(str(settings.public_pair_value.value.get('high', 'high_info')))
                self.p_low.setText(str(settings.public_pair_value.value.get('low', 'low_info')))
                self.pair_info_box.setTitle(
                    ' '.join([
                        self.public_market.combo.currentText(),
                        self.public_pair.combo.currentText().upper(),
                        time.ctime(float(settings.public_pair_value.value.get('updated', 'updated_info')))
                    ]))
            else:
                self.p_sell_price.setText('sell_info')
                self.p_buy_price.setText('buy_info')
                self.p_last.setText('last_info')
                self.p_avg.setText('avg_info')
                self.p_high.setText('high_info')
                self.p_low.setText('low_info')
                self.pair_info_box.setTitle('Pair Info')

        def on_wallet_balance_change():
            text = ''
            if len(settings.selected_wallet_balance.value.keys()) > 0:
                for (k, v) in settings.selected_wallet_balance.value.items():
                    if float(v) > 0:
                        value = '{0:.8f}'.format(v)
                        text = text + "{0}{1}".format(k.ljust(5, ' '), value.rjust(25, ' ')) + "\n"
            # print(settings.selected_wallet_balance.value)
            self.balance_box_textBrowser.setText(text)

        def on_active_orders_change():
            sell_text = ''
            buy_text = ''
            if len(settings.selected_wallet_active_orders.value.keys()) > 0:
                for (order_number, order_params) in settings.selected_wallet_active_orders.value.items():
                    text = f"<{order_number}> {order_params['pair']} :\n" \
                           f"{order_params['amount']} @ {order_params['rate']}"
                    if order_params['type'] == 'sell':
                        sell_text = sell_text + text + '\n'
                    if order_params['type'] == 'buy':
                        buy_text = buy_text + text + '\n'
            self.sell_orders_textBrowser.setText(sell_text)
            self.buy_orders_textBrowser.setText(buy_text)

        settings.public_pair_value.changed.connect(on_public_pair_change)
        settings.selected_wallet_balance.changed.connect(on_wallet_balance_change)
        settings.selected_wallet_active_orders.changed.connect(on_active_orders_change)


if __name__ == '__main__':
    settings.names_of_wallets = Wallets.get_list_of_wallets().value
    settings.supported_pairs = Wallets.value_range_of_parameter('pairs').value

    settings.refresh_data_thread.start()
    trader_app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(trader_app.exec_())

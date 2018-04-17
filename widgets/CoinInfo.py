from time import ctime

from PyQt5 import QtWidgets, QtCore, QtGui

import shared_data


class CoinInfoWidget(QtWidgets.QWidget):
    no_info = '-'
    main_box_defaul_name = 'SYMBOL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_box = QtWidgets.QGroupBox(self.main_box_defaul_name, self)
        self.last = QtWidgets.QLabel(self.no_info, self.main_box)
        self.high = QtWidgets.QLabel(self.no_info, self.main_box)
        self.low = QtWidgets.QLabel(self.no_info, self.main_box)
        self.volume = QtWidgets.QLabel(self.no_info, self.main_box)
        self.change = QtWidgets.QLabel(self.no_info, self.main_box)
        self.change_percent = QtWidgets.QLabel(self.no_info, self.main_box)
        self.server_time = QtWidgets.QLabel(self.no_info, self.main_box)
        self.url = QtWidgets.QLabel(self.no_info, self.main_box)
        self.init_ui()

    def init_ui(self):
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(13)
        blue_palette = QtGui.QPalette()
        blue_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.blue)
        red_palette = QtGui.QPalette()
        red_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)
        green_palette = QtGui.QPalette()
        green_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.darkGreen)

        self.main_box.setGeometry(QtCore.QRect(5, 80, 170, 300))
        # last
        label = QtWidgets.QLabel('Last Price', self.main_box)
        label.setGeometry(QtCore.QRect(10, 20, 150, 15))
        self.last.setGeometry(QtCore.QRect(10, 40, 150, 15))
        self.last.setFont(font)
        self.last.setPalette(green_palette)
        self.last.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # high
        label = QtWidgets.QLabel('24h High', self.main_box)
        label.setGeometry(QtCore.QRect(10, 55, 150, 15))
        self.high.setGeometry(QtCore.QRect(10, 75, 150, 15))
        self.high.setFont(font)
        self.high.setPalette(blue_palette)
        self.high.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # low
        label = QtWidgets.QLabel('24h Low', self.main_box)
        label.setGeometry(QtCore.QRect(10, 90, 150, 15))
        self.low.setGeometry(QtCore.QRect(10, 110, 150, 15))
        self.low.setFont(font)
        self.low.setPalette(blue_palette)
        self.low.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # volume
        label = QtWidgets.QLabel('24h Volume', self.main_box)
        label.setGeometry(QtCore.QRect(10, 125, 150, 15))
        self.volume.setGeometry(QtCore.QRect(10, 145, 150, 15))
        self.volume.setFont(font)
        self.volume.setPalette(blue_palette)
        self.volume.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # change
        label = QtWidgets.QLabel('24h MAX Change', self.main_box)
        label.setGeometry(QtCore.QRect(10, 160, 150, 15))
        self.change.setGeometry(QtCore.QRect(10, 180, 150, 15))
        self.change.setFont(font)
        self.change.setPalette(red_palette)
        self.change.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # change percent
        label = QtWidgets.QLabel('24h MAX % Change', self.main_box)
        label.setGeometry(QtCore.QRect(10, 195, 150, 15))
        self.change_percent.setGeometry(QtCore.QRect(10, 215, 150, 15))
        self.change_percent.setFont(font)
        self.change_percent.setPalette(red_palette)
        self.change_percent.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # server time
        self.server_time.setGeometry(QtCore.QRect(10, self.main_box.geometry().height() - 35, 150, 15))
        self.server_time.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # url market
        self.url.setGeometry(QtCore.QRect(10, self.main_box.geometry().height() - 55, 150, 15))
        self.url.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def update_info(self):
        if len(shared_data.selected_public_pair) > 3:
            coin_from, coin_to = shared_data.selected_public_pair.split('_')
            symbol = f'{coin_from}{coin_to}'.upper()
            self.main_box.setTitle(f'{symbol}')
            data = shared_data.symbol_ticker.value
            self.last.setText('{:0,.2f}'.format(float(data.get('last', 0))))
            self.high.setText('{:0,.2f}'.format(float(data.get('high', 0))))
            self.low.setText('{:0,.2f}'.format(float(data.get('low', 0))))
            self.volume.setText('{:0,.0f}'.format(float(data.get('vol', 0))))
            change = float(data.get('high', 0)) - float(data.get('low', 0))
            self.change.setText('{:0,.2f}'.format(change))
            mavg = (float(data.get('high', 0)) + float(data.get('low', 0))) / 2
            self.change_percent.setText('{:0,.2f} %'.format(change / mavg * 100))
            self.server_time.setText(ctime(float(data.get('updated', 0))))
            self.url.setText(shared_data.selected_public_market)
        else:
            self.main_box.setTitle(self.main_box_defaul_name)

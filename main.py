import sys

from PyQt5 import QtWidgets

from dataproviders.MarketProvider import MarketDataProvider
from dataproviders.TwitterProvider import TweetNewsProvider
from gui.ui import MainWindow

if __name__ == '__main__':

    trader_app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    marketDataProvider = MarketDataProvider()
    marketDataProvider.start()

    twitterDataProvider = TweetNewsProvider()
    twitterDataProvider.start()

    sys.exit(trader_app.exec_())

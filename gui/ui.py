from PyQt5 import QtWidgets, QtCore

from gui.widgets.WidgetForActions import AddWalletWidget, DeleteWalletWidget, AddOrder, DeleteOrder
from gui.widgets.cryptoinformation.WidgetForCryptoCoinInformation import CryptoCoinInformation
from gui.widgets.twitterinformation.WidgetForTwitterNews import TwitterNews
from gui.widgets.walletinformation.WidgetForWalletInformation import WalletInformation


class MainWindow(QtWidgets.QMainWindow):
    shiftFromTop = 30
    shiftFromBorder = 3
    width = None
    height = None

    xOfTopLeftWidget = None
    yOfTopLeftWidget = None
    widthOfTopLeftWidget = None
    heightOfTopLeftWidget = None

    xOfTopRightWidget = None
    yOfTopRightWidget = None
    widthOfTopRightWidget = None
    heightOfTopRightWidget = None

    xOfMiddleLeftWidget = None
    yOfMiddleLeftWidget = None
    widthOfMiddleLeftWidget = None
    heightOfMiddleLeftWidget = None

    xOfMiddleRightWidget = None
    yOfMiddleRightWidget = None
    widthOfMiddleRightWidget = None
    heightOfMiddleRightWidget = None

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.setGeneralOptionsForWindow()
        'public actions'
        self.actionExitApplication = QtWidgets.QAction('Exit', self)
        self.actionWalletCreation = QtWidgets.QAction('Create Wallet ...', self)
        self.actionWalletDestruction = QtWidgets.QAction('Remove Wallet ...', self)
        self.actionOrderCreation = QtWidgets.QAction('Create Order ...', self)
        self.actionOrderCancellation = QtWidgets.QAction('Cancel Order ...', self)
        'widgets on desk'
        self.widgetForCryptoCoinInformation = CryptoCoinInformation(self.xOfTopLeftWidget,
                                                                    self.yOfTopLeftWidget,
                                                                    self.widthOfTopLeftWidget,
                                                                    self.heightOfTopLeftWidget,
                                                                    parent=self)

        self.widgetForTwitterNews = TwitterNews(self.xOfTopRightWidget,
                                                self.yOfTopRightWidget,
                                                self.widthOfTopRightWidget,
                                                self.heightOfTopRightWidget,
                                                parent=self)
        self.widgetForWalletInformation = WalletInformation(self.xOfMiddleLeftWidget,
                                                            self.yOfMiddleLeftWidget,
                                                            self.widthOfMiddleLeftWidget,
                                                            self.heightOfMiddleLeftWidget,
                                                            parent=self)
        'widgets on fly'
        self.widgetForWalletCreation = AddWalletWidget(None)
        self.widgetForWalletDestruction = DeleteWalletWidget(None)
        self.widgetForOrderCreation = AddOrder(None)
        self.widgetForOrderCancellation = DeleteOrder(None)
        'menu'
        self.constructMenu()
        'slots'
        self.setSlots()

    def setGeneralOptionsForWindow(self):
        geometry = QtWidgets.QDesktopWidget().availableGeometry()
        self.width = geometry.width()
        self.height = geometry.height() - self.shiftFromTop
        print("Main Window:", (self.width, self.height))

        self.widthOfTopRightWidget = 250
        self.widthOfTopLeftWidget = self.width - self.widthOfTopRightWidget

        self.xOfTopLeftWidget = 0
        self.xOfMiddleLeftWidget = 0
        self.xOfTopRightWidget = self.xOfTopLeftWidget + self.widthOfTopLeftWidget
        self.yOfTopLeftWidget = 20
        self.yOfTopRightWidget = self.yOfTopLeftWidget
        self.heightOfTopLeftWidget = int((self.height - self.yOfTopLeftWidget) / 2)
        self.yOfMiddleLeftWidget = self.yOfTopLeftWidget + self.heightOfTopLeftWidget

        self.widthOfMiddleLeftWidget = self.width - self.widthOfTopRightWidget
        self.heightOfMiddleLeftWidget = self.height - self.yOfMiddleLeftWidget

        self.heightOfTopRightWidget = self.height - self.yOfTopRightWidget

        self.setGeometry(QtCore.QRect(0,
                                      self.shiftFromTop,
                                      self.width,
                                      self.height
                                      ))
        self.setWindowTitle('TradeMaster')

    def constructMenu(self):
        menu = self.menuBar()
        menuFile = menu.addMenu('&File')
        menuFile.addAction(self.actionExitApplication)
        menuWallet = menu.addMenu('&Wallet')
        menuWallet.addAction(self.actionWalletCreation)
        menuWallet.addAction(self.actionWalletDestruction)
        menuOrders = menu.addMenu('&Orders')
        menuOrders.addAction(self.actionOrderCreation)
        menuOrders.addAction(self.actionOrderCancellation)

    def setSlots(self):
        self.actionExitApplication.triggered.connect(self.close)
        self.actionWalletCreation.triggered.connect(self.widgetForWalletCreation.show)
        self.actionWalletDestruction.triggered.connect(self.widgetForWalletDestruction.show)
        self.actionOrderCreation.triggered.connect(self.widgetForOrderCreation.show)
        self.actionOrderCancellation.triggered.connect(self.widgetForOrderCancellation.show)

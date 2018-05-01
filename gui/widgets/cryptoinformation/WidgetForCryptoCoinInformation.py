from PyQt5 import QtWidgets, QtCore

from gui.widgets.cryptoinformation.WidgetForLiveChart import LiveChart
from gui.widgets.cryptoinformation.WidgetForTickerOfCryptoCoin import TickerOfCryptoCoin
from gui.widgets.cryptoinformation.WidgetForUserChoice import UserChoice


class CryptoCoinInformation(QtWidgets.QWidget):
    shiftFromTop = 20
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

    def __init__(self, x, y, width, height, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shiftFromBorder = self.parent().shiftFromBorder
        self.setGeneralOptionsForWidget()
        self.box = QtWidgets.QGroupBox('Info', self)
        self.setGeometryForWidget()

        self.liveChart = LiveChart(self.xOfTopRightWidget,
                                   self.yOfTopRightWidget,
                                   self.widthOfTopRightWidget,
                                   self.heightOfTopRightWidget,
                                   parent=self.box)
        self.tickerOfCryptoCoin = TickerOfCryptoCoin(self.xOfMiddleLeftWidget,
                                                     self.yOfMiddleLeftWidget,
                                                     self.widthOfMiddleLeftWidget,
                                                     self.heightOfMiddleLeftWidget,
                                                     parent=self.box)
        self.userChoice = UserChoice(self.xOfTopLeftWidget,
                                     self.yOfTopLeftWidget,
                                     self.widthOfTopLeftWidget,
                                     self.heightOfTopLeftWidget,
                                     parent=self.box)

    def setGeneralOptionsForWidget(self):
        self.xOfTopLeftWidget = 0
        self.yOfTopLeftWidget = 0
        self.widthOfTopLeftWidget = 200
        self.heightOfTopLeftWidget = 80

        self.xOfTopRightWidget = self.xOfTopLeftWidget + self.widthOfTopLeftWidget
        self.yOfTopRightWidget = self.yOfTopLeftWidget
        self.widthOfTopRightWidget = self.width - self.xOfTopRightWidget
        self.heightOfTopRightWidget = self.height - self.yOfTopRightWidget

        self.xOfMiddleLeftWidget = self.xOfTopLeftWidget
        self.yOfMiddleLeftWidget = self.yOfTopLeftWidget + self.heightOfTopLeftWidget
        self.widthOfMiddleLeftWidget = self.widthOfTopLeftWidget
        self.heightOfMiddleLeftWidget = self.height - self.yOfMiddleLeftWidget

    def setGeometryForWidget(self):
        print("CryptoCoinInformation: ", (self.x, self.y, self.width, self.height))
        geometry = QtCore.QRect(self.x,
                                self.y,
                                self.width,
                                self.height)
        self.setGeometry(geometry)

        geometry = QtCore.QRect(self.shiftFromBorder,
                                self.shiftFromBorder,
                                self.width - 2 * self.shiftFromBorder,
                                self.height - 2 * self.shiftFromBorder)
        self.box.setGeometry(geometry)

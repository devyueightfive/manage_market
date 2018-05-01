from PyQt5 import QtWidgets, QtCore, QtChart

import sharedData


class LiveChart(QtWidgets.QWidget):
    def __init__(self, x, y, width, height, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shiftFromBorder = self.parent().parent().shiftFromBorder
        self.setGeometryForWidget()
        self.setChart()

    def setChart(self):
        cv = QtChart.QChartView()
        cv.setParent(self)
        cv.setGeometry(0, 7, self.width - 7, self.height - 16)
        cv.setChart(PublicChart())
        cv.setRenderHint(True)

    def setGeometryForWidget(self):
        print("LiveChart: ", (self.x, self.y, self.width, self.height))
        geometry = QtCore.QRect(self.x,
                                self.y,
                                self.width,
                                self.height)
        self.setGeometry(geometry)


class PublicChart(QtChart.QChart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()

    def init(self):
        sharedData.tradePairTrades.changed.connect(self.updateSeriesOnChart)

    def updateSeriesOnChart(self):
        self.removeAllSeries()
        trade_series = QtChart.QLineSeries()
        trade_series.setColor(QtCore.Qt.darkGreen)
        if len(sharedData.tradePairTrades.value) > 2:
            series = []
            for v in sharedData.tradePairTrades.value:
                date = int(v['timestamp']) * 1000
                value = float(v['price'])
                trade_series.append(date, value)
                series.append((date, value))
            # print(series)
            self.addSeries(trade_series)
            self.setTitle(f"{sharedData.marketURLSelectedByUser.upper()}")
            trade_series.setName(sharedData.tradePairSelectedByUser)
        else:
            self.setTitle("<market name>")
            trade_series.setName("<coin_pair>")
        self.createDefaultAxes()
        axis_x = QtChart.QDateTimeAxis()
        axis_x.setFormat("dd-MMM hh:mm")
        axis_x.setTickCount(7)
        self.setAxisX(axis_x, trade_series)

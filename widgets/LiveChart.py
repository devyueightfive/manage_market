from PyQt5 import QtWidgets, QtCore, QtChart

import shared_data


class LiveChart(QtWidgets.QWidget):
    def __init__(self, parent, *args):
        super().__init__(parent, *args)
        self.pair_info_box = QtWidgets.QGroupBox('Live Chart', parent)
        self.init_widget()

    def init_widget(self):
        self.pair_info_box.setGeometry(QtCore.QRect(180, 10, 590, 370))
        cv = QtChart.QChartView()
        cv.setChart(PublicChart())
        cv.setParent(self.pair_info_box)
        cv.setGeometry(5, 15, self.pair_info_box.geometry().width() - 10,
                       self.pair_info_box.geometry().height() - 20)
        cv.setRenderHint(True)


class PublicChart(QtChart.QChart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init()

    def init(self):
        shared_data.trades.changed.connect(self.update_series)

    def update_series(self):
        self.removeAllSeries()
        trade_series = QtChart.QLineSeries()
        trade_series.setColor(QtCore.Qt.darkGreen)
        if len(shared_data.trades.value) > 2:
            series = []
            for v in shared_data.trades.value:
                date = int(v['timestamp']) * 1000
                value = float(v['price'])
                trade_series.append(date, value)
                series.append((date, value))
            # print(series)
            self.addSeries(trade_series)
            self.setTitle(f"{shared_data.selected_public_market.upper()}")
            trade_series.setName(shared_data.selected_public_pair)
        else:
            self.setTitle("<market name>")
            trade_series.setName("<coin_pair>")
        self.createDefaultAxes()
        axis_x = QtChart.QDateTimeAxis()
        axis_x.setFormat("dd-MMM hh:mm")
        self.setAxisX(axis_x, trade_series)

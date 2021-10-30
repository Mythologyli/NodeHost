from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis


class DrawWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 600, 400)
        self.setWindowIcon(QIcon("gml.png"))

        self.humi_series = QLineSeries()
        self.temp_series = QLineSeries()
        self.light_series = QLineSeries()

        ctime = QDateTime.currentDateTime()

        humi_chart = QChart()
        humi_chart.setTheme(QChart.ChartThemeLight)
        humi_chart.addSeries(self.humi_series)
        humi_chart.setTitle("时间-湿度变化曲线")

        temp_chart = QChart()
        temp_chart.setTheme(QChart.ChartThemeLight)
        temp_chart.addSeries(self.temp_series)
        temp_chart.setTitle("时间-温度变化曲线")

        light_chart = QChart()
        light_chart.setTheme(QChart.ChartThemeLight)
        light_chart.addSeries(self.light_series)
        light_chart.setTitle("时间-光照度变化曲线")

        self.humi_dtaxisX = QDateTimeAxis()
        self.temp_dtaxisX = QDateTimeAxis()
        self.light_dtaxisX = QDateTimeAxis()
        self.humi_vlaxisY = QValueAxis()
        self.temp_vlaxisY = QValueAxis()
        self.light_vlaxisY = QValueAxis()
        self.humi_dtaxisX.setMin(ctime.addSecs(0))
        self.humi_dtaxisX.setMax(ctime.addSecs(-60))
        self.temp_dtaxisX.setMin(ctime.addSecs(0))
        self.temp_dtaxisX.setMax(ctime.addSecs(-60))
        self.light_dtaxisX.setMin(ctime.addSecs(0))
        self.light_dtaxisX.setMax(ctime.addSecs(-60))
        self.humi_vlaxisY.setMin(40)
        self.humi_vlaxisY.setMax(50)
        self.temp_vlaxisY.setMin(20)
        self.temp_vlaxisY.setMax(30)
        self.light_vlaxisY.setMin(0)
        self.light_vlaxisY.setMax(100)

        self.humi_dtaxisX.setFormat("hh:mm:ss")
        self.humi_dtaxisX.setTickCount(10)
        self.temp_dtaxisX.setFormat("hh:mm:ss")
        self.temp_dtaxisX.setTickCount(10)
        self.light_dtaxisX.setFormat("hh:mm:ss")
        self.light_dtaxisX.setTickCount(10)
        self.humi_vlaxisY.setTickCount(10)
        self.temp_vlaxisY.setTickCount(10)
        self.light_vlaxisY.setTickCount(1)

        self.humi_dtaxisX.setTitleText("时间")
        self.temp_dtaxisX.setTitleText("时间")
        self.light_dtaxisX.setTitleText("时间")
        self.humi_vlaxisY.setTitleText("湿度")
        self.temp_vlaxisY.setTitleText("温度")
        self.light_vlaxisY.setTitleText("光照度")

        self.humi_vlaxisY.setGridLineVisible(True)
        self.humi_vlaxisY.setGridLineColor(Qt.gray)
        self.temp_vlaxisY.setGridLineVisible(True)
        self.temp_vlaxisY.setGridLineColor(Qt.gray)
        self.light_vlaxisY.setGridLineVisible(True)
        self.light_vlaxisY.setGridLineColor(Qt.gray)
        self.humi_dtaxisX.setGridLineVisible(True)
        self.humi_dtaxisX.setGridLineColor(Qt.gray)
        self.temp_dtaxisX.setGridLineVisible(True)
        self.temp_dtaxisX.setGridLineColor(Qt.gray)
        self.light_dtaxisX.setGridLineVisible(True)
        self.light_dtaxisX.setGridLineColor(Qt.gray)

        humi_chart.addAxis(self.humi_dtaxisX, Qt.AlignBottom)
        humi_chart.addAxis(self.humi_vlaxisY, Qt.AlignLeft)
        temp_chart.addAxis(self.temp_dtaxisX, Qt.AlignBottom)
        temp_chart.addAxis(self.temp_vlaxisY, Qt.AlignLeft)
        light_chart.addAxis(self.light_dtaxisX, Qt.AlignBottom)
        light_chart.addAxis(self.light_vlaxisY, Qt.AlignLeft)

        self.humi_series.attachAxis(self.humi_dtaxisX)
        self.humi_series.attachAxis(self.humi_vlaxisY)
        self.temp_series.attachAxis(self.temp_dtaxisX)
        self.temp_series.attachAxis(self.temp_vlaxisY)
        self.light_series.attachAxis(self.light_dtaxisX)
        self.light_series.attachAxis(self.light_vlaxisY)

        humi_chartview = QChartView(humi_chart)
        temp_chartview = QChartView(temp_chart)
        light_chartview = QChartView(light_chart)

        layout = QGridLayout()
        layout.addWidget(humi_chartview, 1, 1)
        layout.addWidget(temp_chartview, 1, 2)
        layout.addWidget(light_chartview, 2, 1)
        self.setLayout(layout)

        self.node_seq = 2

    def start(self, node_seq: int):
        self.setWindowTitle(f"节点{node_seq}数据监测图")
        self.node_seq = node_seq
        self.show()

    def addPoint(self, node_seq: int, node_data: dict):

        if self.node_seq == node_seq:
            ctime = QDateTime.currentDateTime()
            self.humi_dtaxisX.setMin(ctime.addSecs(-60))
            self.humi_dtaxisX.setMax(ctime.addSecs(0))
            self.temp_dtaxisX.setMin(ctime.addSecs(-60))
            self.temp_dtaxisX.setMax(ctime.addSecs(0))
            self.light_dtaxisX.setMin(ctime.addSecs(-60))
            self.light_dtaxisX.setMax(ctime.addSecs(0))

            if self.humi_vlaxisY.max() - 2 < node_data['humi'] or self.humi_vlaxisY.min() + 2 > node_data['humi']:
                self.humi_vlaxisY.setMin(node_data['humi'] * 0.8)
                self.humi_vlaxisY.setMax(node_data['humi'] * 1.2)

            if self.temp_vlaxisY.max() - 2 < node_data['temp'] or self.temp_vlaxisY.min() + 2 > node_data['temp']:
                self.temp_vlaxisY.setMin(node_data['temp'] * 0.8)
                self.temp_vlaxisY.setMax(node_data['temp'] * 1.2)

            if self.light_vlaxisY.max() - 20 < node_data['light'] or self.light_vlaxisY.min() + 20 > node_data['light']:
                self.light_vlaxisY.setMin(node_data['light'] * 0.8)
                self.light_vlaxisY.setMax(node_data['light'] * 1.2)

            self.humi_series.append(
                ctime.toMSecsSinceEpoch(), node_data['humi'])
            self.temp_series.append(
                ctime.toMSecsSinceEpoch(), node_data['temp'])
            self.light_series.append(
                ctime.toMSecsSinceEpoch(), node_data['light'])

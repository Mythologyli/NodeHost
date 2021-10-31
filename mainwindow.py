import sys

import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from drawwindow import DrawWindow
from aboutwindow import AboutWindow
from serialhandler import SerialHandler


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('NoidHost')
        self.setWindowIcon(QIcon('gml.png'))

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('等待连接')

        menubar = self.menuBar()

        # 菜单栏-文件
        exit_action = QAction('&退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('退出应用')
        exit_action.triggered.connect(lambda: sys.exit())

        menubar_file = menubar.addMenu('文件')
        menubar_file.addAction(exit_action)

        # 菜单栏-校准
        adjust_action = QAction('&校准菜单', self)
        adjust_action.triggered.connect(lambda: sys.exit())

        menubar_adjust = menubar.addMenu('校准')
        menubar_adjust.addAction(adjust_action)

        # 菜单栏-曲线
        draw_node2_action = QAction('&节点2', self)
        draw_node3_action = QAction('&节点3', self)
        draw_node4_action = QAction('&节点4', self)
        draw_node5_action = QAction('&节点5', self)

        self.node2_drawwindow = DrawWindow()
        self.node3_drawwindow = DrawWindow()
        self.node4_drawwindow = DrawWindow()
        self.node5_drawwindow = DrawWindow()

        menubar_draw = menubar.addMenu('曲线')
        menubar_draw.addAction(draw_node2_action)
        menubar_draw.addAction(draw_node3_action)
        menubar_draw.addAction(draw_node4_action)
        menubar_draw.addAction(draw_node5_action)

        draw_node2_action.triggered.connect(
            lambda: self.drawStart(2))
        draw_node3_action.triggered.connect(
            lambda: self.drawStart(3))
        draw_node4_action.triggered.connect(
            lambda: self.drawStart(4))
        draw_node5_action.triggered.connect(
            lambda: self.drawStart(5))

        # 菜单栏-关于
        self.aboutwindow = AboutWindow()
        about_action = QAction('&关于', self)
        about_action.setShortcut('Ctrl+A')
        about_action.setStatusTip('关于')
        about_action.triggered.connect(lambda: self.aboutwindow.show())

        menubar_about = menubar.addMenu('关于')
        menubar_about.addAction(about_action)

        self.label_node2 = QLabel(
            '节点：2    湿度：    %    温度：    °C    光照度：     lx    ')
        self.label_node3 = QLabel(
            '节点：3    湿度：    %    温度：    °C    光照度：     lx    ', self)
        self.label_node4 = QLabel(
            '节点：4    湿度：    %    温度：    °C    光照度：     lx    ', self)
        self.label_node5 = QLabel(
            '节点：5    湿度：    %    温度：    °C    光照度：     lx    ', self)

        self.combobox = QComboBox()

        self.port_list = serial.tools.list_ports.comports()
        for port in self.port_list:
            self.combobox.addItem(port.description)

        self.btnStart = QPushButton('开始')
        self.btnExit = QPushButton('退出')
        self.btnScanPort = QPushButton('刷新串口')

        # 实例化多线程对象
        self.handler = SerialHandler(self.port_list[0].name)

        # 把控件放置在栅格布局中
        layout = QGridLayout()
        layout.addWidget(self.label_node2, 1, 1, 1, 4)
        layout.addWidget(self.label_node3, 2, 1, 1, 4)
        layout.addWidget(self.label_node4, 3, 1, 1, 4)
        layout.addWidget(self.label_node5, 4, 1, 1, 4)
        layout.addWidget(self.btnScanPort, 5, 1, 1, 1)
        layout.addWidget(self.combobox, 5, 2, 1, 1)
        layout.addWidget(self.btnStart, 5, 3, 1, 1)
        layout.addWidget(self.btnExit, 5, 4, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.widget.setStyleSheet("QLabel{font-size: 18pt;}")
        self.setCentralWidget(self.widget)

        # 信号与槽函数的连接
        self.handler.sign_node.connect(self.slotUpdateNode)
        self.combobox.currentIndexChanged.connect(self.slotSelectPort)
        self.btnScanPort.clicked.connect(self.slotScanPort)
        self.btnStart.clicked.connect(self.slotStart)
        self.btnExit.clicked.connect(lambda: sys.exit())

    def slotScanPort(self):
        self.port_list = serial.tools.list_ports.comports()
        self.combobox.clear()
        for port in self.port_list:
            self.combobox.addItem(port.description)
        self.handler.port_name = self.port_list[0].name

    def slotSelectPort(self, index):
        self.handler.port_name = self.port_list[index].name

    def slotUpdateNode(self, node_seq: int, node_data: dict):
        # 更新
        if (node_seq == 2):
            self.label_node2.setText(
                f"节点：2    湿度：{node_data['humi']}%    温度：{node_data['temp']}°C    光照度：{node_data['light']}lx")
        if (node_seq == 3):
            self.label_node3.setText(
                f"节点：3    湿度：{node_data['humi']}%    温度：{node_data['temp']}°C    光照度：{node_data['light']}lx")
        if (node_seq == 4):
            self.label_node4.setText(
                f"节点：4    湿度：{node_data['humi']}%    温度：{node_data['temp']}°C    光照度：{node_data['light']}lx")
        if (node_seq == 5):
            self.label_node5.setText(
                f"节点：5    湿度：{node_data['humi']}%    温度：{node_data['temp']}°C    光照度：{node_data['light']}lx")

    def slotStart(self):
        self.combobox.setEnabled(False)
        self.btnScanPort.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExit.setEnabled(True)
        self.statusbar.showMessage('已连接')
        self.handler.start()

    def drawStart(self, node_seq: int):
        if node_seq == 2:
            self.handler.sign_node.connect(self.node2_drawwindow.addPoint)
            self.node2_drawwindow.start(node_seq)
        elif node_seq == 3:
            self.handler.sign_node.connect(self.node3_drawwindow.addPoint)
            self.node3_drawwindow.start(node_seq)
        elif node_seq == 4:
            self.handler.sign_node.connect(self.node4_drawwindow.addPoint)
            self.node4_drawwindow.start(node_seq)
        elif node_seq == 5:
            self.handler.sign_node.connect(self.node5_drawwindow.addPoint)
            self.node5_drawwindow.start(node_seq)

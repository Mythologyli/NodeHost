import sys
import time
import json

import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setWindowTitle('Demo')

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
        self.thread = Worker(self.port_list[0].name)

        # 把控件放置在栅格布局中
        layout = QGridLayout(self)
        layout.addWidget(self.label_node2, 1, 1, 1, 4)
        layout.addWidget(self.label_node3, 2, 1, 1, 4)
        layout.addWidget(self.label_node4, 3, 1, 1, 4)
        layout.addWidget(self.label_node5, 4, 1, 1, 4)
        layout.addWidget(self.btnScanPort, 6, 1, 1, 1)
        layout.addWidget(self.combobox, 6, 2, 1, 1)
        layout.addWidget(self.btnStart, 6, 3, 1, 1)
        layout.addWidget(self.btnExit, 6, 4, 1, 1)

        # 信号与槽函数的连接
        self.thread.sign_node.connect(self.slotUpdateNode)
        self.combobox.currentIndexChanged.connect(self.slotSelectPort)
        self.btnScanPort.clicked.connect(self.slotScanPort)
        self.btnStart.clicked.connect(self.slotStart)
        self.btnExit.clicked.connect(self.slotStop)

    def slotScanPort(self):
        self.port_list = serial.tools.list_ports.comports()
        self.combobox.clear()
        for port in self.port_list:
            self.combobox.addItem(port.description)
        self.thread.port_name = self.port_list[0].name

    def slotSelectPort(self, index):
        self.thread.port_name = self.port_list[index].name

    def slotUpdateNode(self, node_seq, node_str):
        # 更新
        if (node_seq == 2):
            self.label_node2.setText(node_str)
        if (node_seq == 3):
            self.label_node3.setText(node_str)
        if (node_seq == 4):
            self.label_node4.setText(node_str)
        if (node_seq == 5):
            self.label_node5.setText(node_str)

    def slotStart(self):
        self.combobox.setEnabled(False)
        self.btnScanPort.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnExit.setEnabled(True)
        self.thread.start()

    def slotStop(self):
        self.btnExit.setEnabled(False)
        del self.thread
        sys.exit()


class Worker(QThread):
    sign_node = pyqtSignal(int, str)
    port_name: str

    def __init__(self, port_name, parent=None):
        super(Worker, self).__init__(parent)
        # 设置工作状态与初始num数值
        self.port_name = port_name
        self.working = True

    def __del__(self):
        # 线程状态改变与线程终止
        self.working = False
        self.wait()

    def run(self):
        last_str = ''

        self.com = serial.Serial(self.port_name, 115200)

        while self.working == True:

            serial_str = self.com.readline().decode('utf-8')

            if (serial_str.find('ata') != -1):
                continue

            str_list = serial_str.split('&')  # 分割字符串

            if len(str_list) != 5:  # 数据缺失
                print('数据缺失！')
                continue

            if (serial_str != last_str):  # 检测数据是否重复
                last_str = serial_str

                try:  # 转换数据
                    seq: int = int(str_list[0])
                    humi: float = round(float(str_list[1]), 1)
                    temp: float = round(float(str_list[2]), 1)
                    light: float = round(float(str_list[3]), 1)

                except Exception:
                    print('数据错误！')
                    continue

                print(f"节点：{seq}    湿度：{humi}%    温度：{temp}°C    光照度：{light}lx")

                # 写入 json 文件
                data = json.loads(
                    open('./data.json', 'r', encoding='utf-8').read())

                data['node' + str(seq)]['humi'] = humi
                data['node' + str(seq)]['temp'] = temp
                data['node' + str(seq)]['light'] = light
                data['time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                with open('./data.json', 'w') as fp:
                    fp.write(json.dumps(data))
                    fp.close()

                # 获取文本
                node_str = f"节点：{seq}    湿度：{humi}%    温度：{temp}°C    光照度：{light}lx"
                # 发射信号
                self.sign_node.emit(seq, node_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 18pt;}")
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())

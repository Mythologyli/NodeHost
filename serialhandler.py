import time
import json

import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class SerialHandler(QThread):
    sign_node = pyqtSignal(int, dict)
    port_name: str

    def __init__(self, port_name, parent=None):
        super(SerialHandler, self).__init__(parent)
        self.port_name = port_name
        self.working = True

    def __del__(self):
        # 线程状态改变与线程终止
        self.working = False
        self.wait()

    def run(self):
        last_str = ''  # 记录上一次收到的字符串
        self.com = serial.Serial(self.port_name, 115200)

        while self.working == True:

            serial_str = self.com.readline().decode('utf-8')
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

                # 检测数据合理性
                if humi > 100 or temp > 50 or light > 100000:
                    print('数据不合理！')
                    continue

                # 修正读数
                config = json.loads(
                    open('./config.json', 'r', encoding='utf-8').read())
                humi += config['node' + str(seq)]['humi']
                temp += config['node' + str(seq)]['temp']
                light += config['node' + str(seq)]['light']

                humi = round(humi, 2)
                temp = round(temp, 2)
                light = round(light, 2)

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
                node_data = {
                    "seq": seq,
                    "humi": humi,
                    "temp": temp,
                    "light": light
                }
                # 发射信号
                self.sign_node.emit(seq, node_data)

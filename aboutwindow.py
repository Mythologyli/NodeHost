from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class AboutWindow(QWidget):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)

        self.setWindowTitle('关于')
        self.setWindowIcon(QIcon('gml.png'))
        self.setStyleSheet("QTextBrowser{font-size: 12pt;}")

        self.textbrowser = QTextBrowser()
        self.textbrowser.setHtml(
            '<center><b>NodeHost</b></center><br>' +
            '<br>' +
            '本软件为分布式环境监测系统的上位机软件<br>' +
            '由 GML-Group 制作'
        )

        layout = QHBoxLayout()
        layout.addWidget(self.textbrowser)
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

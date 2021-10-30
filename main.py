import sys
import ctypes

from PyQt5.QtWidgets import *

from mainwindow import MainWindow


if __name__ == '__main__':
    # 防止系统显示为 Python 图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("NoidHost")

    app = QApplication(sys.argv)
    main_widget = MainWindow()
    main_widget.show()
    sys.exit(app.exec_())

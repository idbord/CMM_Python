# -*- coding: utf-8 -*-
__author__ = 'idbord'

from PyQt5 import QtWidgets
from ui.main import Ui_main
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_main()
    ui.setupUi(MainWindow)
    ui.bind_event()
    MainWindow.show()
    sys.exit(app.exec_())

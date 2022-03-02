from PyQt5.QtWidgets import *
from myutil import global_var as gl
from loguru import logger
from ui.main import Ui_MainWindow as main_window


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.setupUi(self)
        logger.info("进入主程序窗口")

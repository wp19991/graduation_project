import os

from PyQt5.QtWidgets import *
from myutil import global_var as gl
from loguru import logger
from ui.main import Ui_MainWindow as main_window
from win.sound_recording_form import sound_recording_win


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.srw = None  # 录音窗口
        self.setupUi(self)
        logger.info("进入主程序窗口")

        # 工具-录音窗口 action 设置
        self.action_sound_recording.triggered.connect(self.action_sound_recording_event)

        # 弹出窗口设置
        self.is_dockWidget_open = dict()

        # 弹出的录音窗口
        self.dockWidget.hide()
        self.is_dockWidget_open["dockWidget"] = False
        self.action_show_dockWidget.triggered.connect(self.action_show_dockWidget_event)

    def action_sound_recording_event(self):
        logger.info("录音窗口")
        if self.srw is not None:
            self.srw.destroy(True)
        self.srw = sound_recording_win()
        self.srw.show()

    def action_show_dockWidget_event(self):
        logger.info("设置弹出窗口的开关")
        if self.is_dockWidget_open["dockWidget"]:
            self.dockWidget.hide()
            self.is_dockWidget_open["dockWidget"] = False
        else:
            self.dockWidget.show()
            self.is_dockWidget_open["dockWidget"] = True

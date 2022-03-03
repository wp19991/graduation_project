import os.path

from PyQt5.QtWidgets import *
from myutil import global_var as gl
from loguru import logger
from ui.main import Ui_MainWindow as main_window


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.setupUi(self)
        logger.info("进入主程序窗口")

        # 弹出窗口设置
        self.is_dockWidget_open = dict()

        # 弹出的录音窗口
        self.sound_recording_dockWidget.hide()
        self.is_dockWidget_open["sound_recording_dockWidget"] = False
        self.action_show_sound_recording.triggered.connect(self.action_show_sound_recording_event)
        # 保存文件的路径按钮设置
        self.sound_recording_save_path_pushButton.clicked.connect(self.sound_recording_save_path_event)
        self.sound_recording_save_path_lineEdit.setText(os.getcwd())
        # 录音窗口的按钮设置
        self.sound_recording_save_path_start_pushButton.clicked.connect(self.sound_recording_save_path_start_event)
        self.sound_recording_save_path_end_pushButton.clicked.connect(self.sound_recording_save_path_end_event)

    def sound_recording_save_path_event(self):
        logger.info("保存文件的路径按钮设置")

        pass

    def sound_recording_save_path_start_event(self):
        logger.info("开始录音")
        self.widget.setVisible(True)
        self.sound_recording_save_path_start_pushButton.setEnabled(False)
        self.sound_recording_save_path_end_pushButton.setEnabled(True)
        self.widget.start_audio()  # 触发MatplotlibWidget的startAudio函数

    def sound_recording_save_path_end_event(self):
        logger.info("结束录音")
        self.sound_recording_save_path_start_pushButton.setEnabled(True)
        self.sound_recording_save_path_end_pushButton.setEnabled(False)
        self.widget.endAudio(save_path=os.getcwd())  # 触发MatplotlibWidget的endAudio函数

    def action_show_sound_recording_event(self):
        logger.info("设置录音窗口的开关")
        if self.is_dockWidget_open["sound_recording_dockWidget"] == True:
            self.sound_recording_dockWidget.hide()
            self.is_dockWidget_open["sound_recording_dockWidget"] = False
        else:
            self.sound_recording_dockWidget.show()
            self.is_dockWidget_open["sound_recording_dockWidget"] = True

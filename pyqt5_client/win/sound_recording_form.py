from PyQt5.QtWidgets import *
import os
from loguru import logger
from ui.sound_recording_frame import Ui_Frame as sound_recording_frame


class sound_recording_win(QWidget, sound_recording_frame):
    def __init__(self, parent=None):
        super(sound_recording_win, self).__init__(parent)
        self.setupUi(self)

        # 保存文件的路径按钮设置
        self.sound_recording_save_path_pushButton.clicked.connect(self.sound_recording_save_path_event)
        self.sound_recording_save_path_lineEdit.setText(os.getcwd())
        # 录音窗口的按钮设置
        self.sound_recording_save_path_start_pushButton.clicked.connect(self.sound_recording_save_path_start_event)
        self.sound_recording_save_path_end_pushButton.clicked.connect(self.sound_recording_save_path_end_event)

    def sound_recording_save_path_event(self):
        logger.info("保存文件的路径按钮设置")
        filePath = QFileDialog.getExistingDirectory(self, "选择存储路径")
        self.sound_recording_save_path_lineEdit.setText(filePath)

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
        self.widget.endAudio(save_path=self.sound_recording_save_path_lineEdit.text())  # 触发MatplotlibWidget的endAudio函数

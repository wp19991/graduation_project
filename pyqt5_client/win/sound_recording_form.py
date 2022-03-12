import datetime

# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QFileDialog
import os
from loguru import logger
from ui.sound_recording_frame import Ui_Frame as sound_recording_frame


class sound_recording_win(QWidget, sound_recording_frame):
    def __init__(self, parent=None):
        super(sound_recording_win, self).__init__(parent)
        self.setupUi(self)

        # 保存文件的路径按钮设置
        self.sound_recording_save_path_pushButton.clicked.connect(self.sound_recording_save_path_event)
        self.sound_recording_save_path_lineEdit.setText(os.path.join(os.path.expanduser("~"), 'Desktop'))

        # 设置保存文件名
        self.save_name_pushButton.clicked.connect(self.save_name_event)
        time1_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M_%S')
        self.save_name_lineEdit.setText(time1_str)

        # 默认的保存路径显示
        self.show_save_path_label.setText(
            "文件保存在：" + os.path.join(os.path.expanduser("~"), 'Desktop') + "\\" + time1_str + ".wav")

        # 录音窗口的按钮设置
        self.sound_recording_save_path_start_pushButton.clicked.connect(self.sound_recording_save_path_start_event)
        self.sound_recording_save_path_end_pushButton.clicked.connect(self.sound_recording_save_path_end_event)

    def save_name_event(self):
        self.show_save_path_label.setText(
            "文件保存在：" + self.sound_recording_save_path_lineEdit.text() + "\\" + self.save_name_lineEdit.text() + ".wav")
        pass

    def sound_recording_save_path_event(self):
        logger.info("保存文件的路径按钮设置")
        filePath = QFileDialog.getExistingDirectory(self, "选择存储路径", os.path.join(os.path.expanduser("~"), 'Desktop'))
        if filePath == "":
            logger.error("请选择路径")
            return
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
        save_path = os.path.join(self.sound_recording_save_path_lineEdit.text(),
                                 self.save_name_lineEdit.text() + ".wav")
        print(save_path)
        self.widget.endAudio(save_path=save_path)  # 触发MatplotlibWidget的endAudio函数

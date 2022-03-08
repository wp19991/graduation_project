import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from myutil import global_var as gl
from loguru import logger
from ui.main import Ui_MainWindow as main_window
from win.sound_recording_form import sound_recording_win
from win.about_form import about_win
from win.help_form import help_win


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.srw = None  # 录音窗口
        self.aw = None  # 录音窗口
        self.hw = None  # 录音窗口
        self.setupUi(self)
        logger.info("进入主程序窗口")

        # 工具-录音窗口 action 设置
        self.action_sound_recording.triggered.connect(self.action_sound_recording_event)
        # 帮助-关于窗口 action 设置
        self.action_about.triggered.connect(self.action_about_event)
        # 帮助-帮助窗口 action 设置
        self.action_help.triggered.connect(self.action_help_event)

        # 按钮事件绑定
        self.save_model_file_path_pushButton.clicked.connect(self.save_model_file_path_event)
        self.need_enh_wav_file_path_pushButton.clicked.connect(self.need_enh_wav_file_path_event)
        self.save_path_pushButton.clicked.connect(self.save_path_event)
        self.enh_pushButton.clicked.connect(self.enh_event)
        self.paly_wav_file_pushButton.clicked.connect(self.paly_wav_file_event)
        self.paly_enh_wav_file_pushButton.clicked.connect(self.paly_enh_wav_file_event)

    def save_model_file_path_event(self):
        logger.info("选择模型文件按钮设置")
        filePath = QFileDialog.getOpenFileName(self, "请选择要添加的文件", os.getcwd(), "pkl Files (*.pkl);;All Files (*)")
        self.save_model_file_path_lineEdit.setText(filePath[0])

    def need_enh_wav_file_path_event(self):
        logger.info("选择需要增强的语音文件按钮设置")
        filePath = QFileDialog.getOpenFileName(self, "请选择要添加的文件", os.getcwd(), "wav Files (*.wav);;All Files (*)")
        if filePath[1] == 'All Files (*)':
            # 如果是别的类型的文件
            # 先转换为wav文件
            # 然后保存到那个目录下面
            # 然后选择那个目录文件夹下的wav文件
            pass
        self.need_enh_wav_file_path_lineEdit.setText(filePath[0])

    def save_path_event(self):
        logger.info("设置文件保存的路径按钮设置")
        savePath = QFileDialog.getExistingDirectory(self, "设置文件保存的路径", os.getcwd())
        self.save_path_lineEdit.setText(savePath)

    def enh_event(self):
        logger.info("进行语音增强的按钮设置")
        # 判断上面的路径是否存在

        # 获得三个路径
        # --model_file=save/model.pkl --noisy_file=wav/p232_010.wav --save_path=ss
        # 命令行调用use.exe进行增强
        self.process(model_file=self.save_model_file_path_lineEdit.text(),
                noisy_file=self.need_enh_wav_file_path_lineEdit.text(),
                save_path=self.save_path_lineEdit.text())

        # 更新进度条

        # 结束之后更新数据显示，和plt的显示

        pass

    def process(self, model_file, noisy_file, save_path):
        QtCore.QProcess.startDetached(r"C:\Users\wp\Desktop\pytorch_SEGAN_core\use.exe",
                                      ["-m", model_file, "-n", noisy_file,
                                       "--save_path", save_path])

    def paly_wav_file_event(self):
        pass

    def paly_enh_wav_file_event(self):
        pass

    def action_sound_recording_event(self):
        logger.info("录音窗口")
        if self.srw is not None:
            self.srw.destroy(True)
        self.srw = sound_recording_win()
        self.srw.show()

    def action_about_event(self):
        logger.info("关于窗口")
        if self.aw is not None:
            self.aw.destroy(True)
        self.aw = about_win()
        self.aw.show()

    def action_help_event(self):
        logger.info("帮助窗口")
        if self.hw is not None:
            self.hw.destroy(True)
        self.hw = help_win()
        self.hw.show()

import os
import time
from threading import Thread

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from myutil import global_var as gl
from loguru import logger

from speech_enhancement_core.pytorch_SEGAN.use import get_and_save_enh
from speech_enhancement_core.specsub.sub_spec import specsub
from ui.main import Ui_MainWindow as main_window
from win.sound_recording_form import sound_recording_win
from win.about_form import about_win
from win.help_form import help_win


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    jdt = pyqtSignal(QProgressBar, int)


# 实例化
global_ms = MySignals()


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.srw = None  # 录音窗口
        self.aw = None  # 录音窗口
        self.hw = None  # 录音窗口
        self.enh_wav_path = None
        self.noisy_wav_path = None
        self.plt_jpg_path = None
        self.setupUi(self)
        logger.info("进入主程序窗口")

        # 定义进度条
        # 设置进度条的范围，参数1为最小值，参数2为最大值（可以调得更大，比如1000
        self.enh_progressBar.setRange(0, 100)
        # 设置进度条的初始值
        self.enh_progressBar.setValue(0)

        # 自定义信号的处理函数
        global_ms.jdt.connect(self.change_jdt)

        # 工具-录音窗口 action 设置
        self.action_sound_recording.triggered.connect(self.action_sound_recording_event)
        # 帮助-关于窗口 action 设置
        self.action_about.triggered.connect(self.action_about_event)
        # 帮助-帮助窗口 action 设置
        self.action_help.triggered.connect(self.action_help_event)

        # 模型驱动文件
        self.pytorch_SEGAN_exe_path = "./speech_enhancement_core/pytorch_SEGAN/use.exe"

        # 默认模型输入
        if os.path.exists("./speech_enhancement_core/pytorch_SEGAN/model.pkl"):
            self.save_model_file_path_lineEdit.setText("./speech_enhancement_core/pytorch_SEGAN/model.pkl")

        # 按钮事件绑定
        self.save_model_file_path_pushButton.clicked.connect(self.save_model_file_path_event)
        self.need_enh_wav_file_path_pushButton.clicked.connect(self.need_enh_wav_file_path_event)
        self.save_path_pushButton.clicked.connect(self.save_path_event)
        self.enh_pushButton.clicked.connect(self.enh_event)
        self.update_data_pushButton.clicked.connect(self.update_data_event)
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
        if not os.path.exists(self.save_model_file_path_lineEdit.text()):
            logger.error("没有这个文件:{}，请重新选择".format(self.save_model_file_path_lineEdit.text()))
            return
        if not os.path.exists(self.need_enh_wav_file_path_lineEdit.text()):
            logger.error("没有这个文件:{}，请重新选择".format(self.need_enh_wav_file_path_lineEdit.text()))
            return
        if not os.path.exists(self.save_path_lineEdit.text()):
            logger.error("没有这个文件夹:{}，请重新选择".format(self.save_path_lineEdit.text()))
            return

        # 调用线程，进行增强,并且更新进度条
        thread = Thread(target=self.threadFunc)
        thread.start()

    def update_data_event(self):
        logger.info("更新数据显示，和plt的显示的按钮设置")
        self.enh_wav_path = os.path.join(self.save_path_lineEdit.text(), "enh-" + os.path.splitext(
            os.path.split(self.need_enh_wav_file_path_lineEdit.text())[1])[
            0] + ".wav")
        self.noisy_wav_path = os.path.join(self.save_path_lineEdit.text(), "noisy-" + os.path.splitext(
            os.path.split(self.need_enh_wav_file_path_lineEdit.text())[1])[
            0] + ".wav")
        self.plt_jpg_path = os.path.join(self.save_path_lineEdit.text(), os.path.splitext(
            os.path.split(self.need_enh_wav_file_path_lineEdit.text())[1])[
            0] + ".jpg")

        self.enh_show_data_label.setText("训练文件保存在：{}".format(self.save_path_lineEdit.text()))
        jpg = QPixmap(self.plt_jpg_path).scaled(self.enh_wav_plt_label.width(), self.enh_wav_plt_label.height())
        self.enh_wav_plt_label.setPixmap(jpg)

    def change_jdt(self, jdt, num):
        jdt.setValue(num)

    def threadFunc(self):
        try:
            # 获得三个路径
            # --model_file=save/model.pkl --noisy_file=wav/p232_010.wav --save_path=ss
            # 进行增强
            get_and_save_enh(model_file=self.save_model_file_path_lineEdit.text(),
                             noisy_file=self.need_enh_wav_file_path_lineEdit.text(),
                             save_path=self.save_path_lineEdit.text())

            a = specsub(noisy_wav_file_path=self.need_enh_wav_file_path_lineEdit.text())
            a.fit()
            a.plt_save(output_path=self.save_path_lineEdit.text())
            a.output_file(wav_file_output_path=self.save_path_lineEdit.text())

            # 更新进度条
            step = 0
            while os.path.exists(os.path.join(self.save_path_lineEdit.text(),
                                              os.path.splitext(
                                                  os.path.split(self.need_enh_wav_file_path_lineEdit.text())[1])[
                                                  0] + ".jpg")) == False:
                return

            step = 0
            need = 100 - step
            for i in range(20):
                time.sleep(0.1)
                global_ms.jdt.emit(self.enh_progressBar, step + need / 20 * i)
            global_ms.jdt.emit(self.enh_progressBar, 100)
        except:
            global_ms.jdt.emit(self.enh_progressBar, 100)

    # def process(self, model_file, noisy_file, save_path):
    #     QtCore.QProcess.startDetached(self.pytorch_SEGAN_exe_path,
    #                                   ["-m", model_file, "-n", noisy_file,
    #                                    "--save_path", save_path])

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

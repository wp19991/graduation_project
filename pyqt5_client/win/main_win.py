import os
import shutil
import time
import wave

import numpy as np
import pyaudio
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from pydub import AudioSegment

from loguru import logger

from speech_enhancement_core.SEGAN.SEGAN import get_and_save_enh
from speech_enhancement_core.specsub.sub_spec import specsub
from ui.main import Ui_MainWindow as main_window
from win.sound_recording_form import sound_recording_win
from win.about_form import about_win
from win.help_form import help_win


class main_data:
    def __init__(self, model_name="深度神经网络_SEGAN"):
        self.model = {"深度神经网络_SEGAN": 0, "维纳滤波_spec_sub": 1}
        self.now_model = self.model[model_name]
        self.model_path = None
        self.noisy_wav_path = None
        self.noisy_wav_data = None
        self.enh_wav_path = None
        self.enh_wav_data = None
        self.save_path = None
        self.plt_save_path = None


# 自定义信号线程类，一定要继承自 QObject
class enh_SEGAN_thread(QThread):
    # 定义一种信号，两个参数 类型分别是： QProgressBar 和 int
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    jdt = pyqtSignal(int)

    def __init__(self, parent=None):
        super(enh_SEGAN_thread, self).__init__(parent)
        self.save_model_file_path = None
        self.need_enh_wav_file_path = None
        self.save_path = None

    def set_path(self, save_model_file_path, need_enh_wav_file_path, save_path):
        self.save_model_file_path = save_model_file_path
        self.need_enh_wav_file_path = need_enh_wav_file_path
        self.save_path = save_path
        self.start()

    def run(self):
        try:
            self.jdt.emit(0)
            # 更新进度条
            step = 0

            # 获得三个路径,进行增强
            enh_wav_path = get_and_save_enh(model_file=self.save_model_file_path,
                                            noisy_file=self.need_enh_wav_file_path,
                                            output_path=self.save_path)

            need = 100
            for i in range(20):
                time.sleep(0.1)
                self.jdt.emit(step + need / 20 * i)
            self.jdt.emit(100)
        except:
            self.jdt.emit(100)
        pass


# 自定义信号线程类，一定要继承自 QObject
class enh_spec_sub_thread(QThread):
    # 定义一种信号，两个参数 类型分别是： QProgressBar 和 int
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    jdt = pyqtSignal(int)

    def __init__(self, parent=None):
        super(enh_spec_sub_thread, self).__init__(parent)
        self.need_enh_wav_file_path = None
        self.save_path = None

    def set_path(self, need_enh_wav_file_path, save_path):
        self.need_enh_wav_file_path = need_enh_wav_file_path
        self.save_path = save_path
        self.start()

    def run(self):
        try:
            self.jdt.emit(0)
            # 更新进度条
            step = 0

            # 获得三个路径,进行增强
            a = specsub(noisy_wav_file_path=self.need_enh_wav_file_path)
            a.fit()
            enh_wav_path = a.output_file(output_path=self.save_path)

            need = 100 - step
            for i in range(20):
                time.sleep(0.1)
                self.jdt.emit(step + need / 20 * i)
            self.jdt.emit(100)
        except:
            self.jdt.emit(100)
        pass


class main_win(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(main_win, self).__init__(parent)
        self.setupUi(self)
        logger.info("进入主程序窗口")

        self.srw = None  # 录音窗口
        self.aw = None  # 关于窗口
        self.hw = None  # 帮助窗口

        # 这个窗口的数据结构
        self.main_data = None

        # 几个QWidgets
        self.figure = plt.figure()  # 可选参数,facecolor为背景颜色
        self.canvas = FigureCanvas(self.figure)

        # 开始隐藏窗口
        self.enh_wav_plt_label.hide()

        # 选择模式
        self.choose_model_comboBox.currentTextChanged.connect(self.choose_model_comboBox_event)

        # 工具-录音窗口 action 设置
        self.action_sound_recording.triggered.connect(self.action_sound_recording_event)
        # 帮助-关于窗口 action 设置
        self.action_about.triggered.connect(self.action_about_event)
        # 帮助-帮助窗口 action 设置
        self.action_help.triggered.connect(self.action_help_event)

        # 默认模型输入
        self.main_data = main_data("深度神经网络_SEGAN")
        if os.path.exists("./speech_enhancement_core/SEGAN/model.pkl"):
            self.save_model_file_path_lineEdit.setText("./speech_enhancement_core/SEGAN/model.pkl")
            self.main_data.model_path = "./speech_enhancement_core/SEGAN/model.pkl"

        # 按钮事件绑定
        self.save_model_file_path_pushButton.clicked.connect(self.save_model_file_path_event)
        self.need_enh_wav_file_path_pushButton.clicked.connect(self.need_enh_wav_file_path_event)
        self.save_path_pushButton.clicked.connect(self.save_path_event)
        self.enh_pushButton.clicked.connect(self.enh_event)
        self.update_data_pushButton.clicked.connect(self.update_data_event)
        self.paly_wav_file_pushButton.clicked.connect(self.play_wav_file_event)
        self.paly_enh_wav_file_pushButton.clicked.connect(self.play_enh_wav_file_event)

        # 定义进度条
        # 设置进度条的范围，参数1为最小值，参数2为最大值（可以调得更大，比如1000
        self.enh_progressBar.setRange(0, 100)
        # 设置进度条的初始值
        self.enh_progressBar.setValue(0)

    def get_5_from_wav_file_path(self, wav_path):

        f = wave.open(wav_path, 'rb')
        # 得到语音参数
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]

        # 将字符串格式的数据转成int型
        strData = f.readframes(nframes)
        waveData = np.fromstring(strData, dtype=np.short)

        # 归一化
        # waveData = waveData * 1.0 / max(abs(waveData))

        # 将音频信号规整乘每行一路通道信号的格式，即该矩阵一行为一个通道的采样点，共nchannels行
        waveData = np.reshape(waveData, [nframes, nchannels]).T  # .T 表示转置
        f.close()  # 关闭文件

        framelength = 0.025  # 帧长20~30ms
        framesize = framelength * framerate  # 每帧点数 N = t*fs,通常情况下值为256或512,要与NFFT相等\
        # 而NFFT最好取2的整数次方,即framesize最好取的整数次方

        # 找到与当前framesize最接近的2的正整数次方
        nfftdict = {}
        lists = [32, 64, 128, 256, 512, 1024]
        for i in lists:
            nfftdict[i] = abs(framesize - i)
        sortlist = sorted(nfftdict.items(), key=lambda x: x[1])  # 按与当前framesize差值升序排列
        framesize = int(sortlist[0][0])  # 取最接近当前framesize的那个2的正整数次方值为新的framesize

        NFFT = framesize  # NFFT必须与时域的点数framsize相等，即不补零的FFT
        overlapSize = 1.0 / 3 * framesize  # 重叠部分采样点数overlapSize约为每帧点数的1/3~1/2
        overlapSize = int(round(overlapSize))  # 取整
        # print("帧长为{},帧叠为{},傅里叶变换点数为{}".format(framesize, overlapSize, NFFT))
        return waveData, NFFT, framerate, framesize, overlapSize

    def plt_save(self):
        name = None
        noisy_waveData = None
        noisy_NFFT = None
        noisy_framerate = None
        noisy_framesize = None
        noisy_overlapSize = None

        enh_waveData = None
        enh_NFFT = None
        enh_framerate = None
        enh_framesize = None
        enh_overlapSize = None

        if self.main_data.now_model == self.main_data.model["维纳滤波_spec_sub"]:
            noisy_waveData, noisy_NFFT, noisy_framerate, noisy_framesize, noisy_overlapSize = self.get_5_from_wav_file_path(
                wav_path=self.main_data.noisy_wav_path)
            enh_waveData, enh_NFFT, enh_framerate, enh_framesize, enh_overlapSize = self.get_5_from_wav_file_path(
                wav_path=self.main_data.enh_wav_path)

            # 绘制噪音的谱图
            name = "noisy_spec_sub_specgram_" + os.path.basename(self.main_data.noisy_wav_path) + ".png"
            # print(name)
        elif self.main_data.now_model == self.main_data.model["深度神经网络_SEGAN"]:
            noisy_waveData, noisy_NFFT, noisy_framerate, noisy_framesize, noisy_overlapSize = self.get_5_from_wav_file_path(
                wav_path=self.main_data.noisy_wav_path)
            enh_waveData, enh_NFFT, enh_framerate, enh_framesize, enh_overlapSize = self.get_5_from_wav_file_path(
                wav_path=self.main_data.enh_wav_path)

            # 绘制噪音的谱图
            name = "noisy_SEGAN_specgram_" + os.path.basename(self.main_data.noisy_wav_path) + ".png"

            # print(name)
        fig_name = self.main_data.save_path + "/" + name
        # print(fig_name)
        # 设置标题
        plt.title(name)

        plt.subplot(2, 1, 1)
        plt.specgram(noisy_waveData[0], NFFT=noisy_NFFT, Fs=noisy_framerate, window=np.hanning(M=noisy_framesize),
                     noverlap=noisy_overlapSize,
                     mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)
        plt.xlabel("before specgram")
        plt.ylim((0, 2000))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=0, hspace=0.8)

        # plt.subplot(3, 1, 2)
        # plt.specgram(np.array(noisy_waveData[0] - enh_waveData[0]), NFFT=noisy_NFFT, Fs=noisy_framerate,
        #              window=np.hanning(M=noisy_framesize), noverlap=noisy_overlapSize,
        #              mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)
        # plt.xlabel("background noisy specgram")
        # plt.ylim((0, 2000))
        # plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
        #                     wspace=0, hspace=0.8)

        plt.subplot(2, 1, 2)
        plt.specgram(enh_waveData[0], NFFT=enh_NFFT, Fs=enh_framerate, window=np.hanning(M=enh_framesize),
                     noverlap=enh_overlapSize,
                     mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)
        plt.xlabel("enhece after specgram")
        plt.ylim((0, 2000))

        # 画图
        self.canvas.draw()
        # 保存画出来的图片
        plt.savefig(fig_name)
        plt.clf()
        self.main_data.plt_save_path = fig_name

    def choose_model_comboBox_event(self):
        if self.choose_model_comboBox.currentText() == "维纳滤波_spec_sub":
            self.main_data = main_data("维纳滤波_spec_sub")
            self.need_enh_wav_file_path_lineEdit.setText("")
            self.save_path_lineEdit.setText("")
            self.label.hide()
            self.save_model_file_path_lineEdit.hide()
            self.save_model_file_path_pushButton.hide()
        elif self.choose_model_comboBox.currentText() == "深度神经网络_SEGAN":
            self.main_data = main_data("深度神经网络_SEGAN")
            if os.path.exists("./speech_enhancement_core/SEGAN/model.pkl"):
                self.save_model_file_path_lineEdit.setText("./speech_enhancement_core/SEGAN/model.pkl")
                self.main_data.model_path = "./speech_enhancement_core/SEGAN/model.pkl"
            self.label.show()
            self.save_model_file_path_lineEdit.show()
            self.save_model_file_path_pushButton.show()

    def save_model_file_path_event(self):
        logger.info("选择模型文件按钮设置")
        filePath = QFileDialog.getOpenFileName(self, "请选择要添加的文件", os.path.join(os.path.expanduser("~"), 'Desktop'), "pkl Files (*.pkl);;All Files (*)")
        if filePath == "":
            logger.error("请选择路径")
            return
        self.save_model_file_path_lineEdit.setText(filePath[0])
        self.main_data.model_path = filePath[0]

    def need_enh_wav_file_path_event(self):
        logger.info("选择需要增强的语音文件按钮设置")
        filePath = QFileDialog.getOpenFileName(self, "请选择要添加的文件", os.path.join(os.path.expanduser("~"), 'Desktop'), "wav Files (*.wav);;All Files (*)")
        if filePath == "":
            logger.error("请选择路径")
            return
        if filePath[1] == 'All Files (*)':
            # 如果是别的类型的文件mp3
            # 先转换为wav文件
            # 然后保存到那个目录下面
            # 然后选择那个目录文件夹下的wav文件

            # 读取mp3的波形数据
            sound = AudioSegment.from_file(filePath, format='MP3')
            # 将读取的波形数据转化为wav
            f = wave.open(filePath + ".wav", 'wb')
            f.setnchannels(1)  # 频道数
            f.setsampwidth(2)  # 量化位数
            f.setframerate(16000)  # 取样频率
            f.setnframes(len(sound._data))  # 取样点数，波形数据的长度
            f.writeframes(sound._data)  # 写入波形数据
            f.close()

            self.need_enh_wav_file_path_lineEdit.setText(filePath[0] + ".wav")
            return
        logger.info("need_enh_wav_file_path=" + filePath[0])
        self.need_enh_wav_file_path_lineEdit.setText(filePath[0])
        self.main_data.noisy_wav_path = filePath[0]

    def save_path_event(self):
        logger.info("设置文件保存的路径按钮设置")
        savePath = QFileDialog.getExistingDirectory(self, "设置文件保存的路径", os.path.join(os.path.expanduser("~"), 'Desktop'))
        self.save_path_lineEdit.setText(savePath)
        self.main_data.save_path = savePath

    def enh_event(self):
        logger.info("进行语音增强的按钮设置")
        # 判断上面的路径是否存在
        if not os.path.exists(self.main_data.noisy_wav_path):
            logger.error("没有这个文件:{}，请重新选择".format(self.main_data.noisy_wav_path))
            return
        if not os.path.exists(self.main_data.save_path):
            logger.error("没有这个文件夹:{}，请重新选择".format(self.main_data.save_path))
            return

        # 将噪音文件复制到保存的目录下面
        # 将指定的文件file复制到file_dir的文件夹里面
        shutil.copy(self.main_data.noisy_wav_path, self.main_data.save_path)

        if self.main_data.now_model == self.main_data.model["维纳滤波_spec_sub"]:
            # 设置路径
            self.main_data.enh_wav_path = self.main_data.save_path + "/" + "noisy_sub_spec_enhance_" + \
                                          os.path.basename(self.main_data.noisy_wav_path)

            # 创建线程
            self.global_1 = enh_spec_sub_thread()
            # 连接信号
            self.global_1.jdt.connect(self.change_jdt)
            # 调用线程，进行增强,并且更新进度条
            self.global_1.set_path(need_enh_wav_file_path=self.main_data.noisy_wav_path,
                                   save_path=self.main_data.save_path)
        elif self.main_data.now_model == self.main_data.model["深度神经网络_SEGAN"]:
            if not os.path.exists(self.main_data.model_path):
                logger.error("没有这个文件:{}，请重新选择".format(self.main_data.model_path))
                return
            # 设置路径
            self.main_data.enh_wav_path = self.main_data.save_path + "/" + "noisy_SEGAN_enhance_" + \
                                          os.path.basename(self.main_data.noisy_wav_path)
            # 创建线程
            self.global_0 = enh_SEGAN_thread()
            # 连接信号
            self.global_0.jdt.connect(self.change_jdt)
            # 调用线程，进行增强,并且更新进度条
            self.global_0.set_path(save_model_file_path=self.main_data.model_path,
                                   need_enh_wav_file_path=self.main_data.noisy_wav_path,
                                   save_path=self.main_data.save_path)
        self.update_data_pushButton.setEnabled(True)

    def change_jdt(self, num):
        self.enh_progressBar.setValue(num)

    def update_data_event(self):
        logger.info("更新数据显示，和plt的显示的按钮设置")
        self.plt_save()

        self.enh_show_data_label.setText("增强文件保存在：{}".format(self.main_data.save_path))
        jpg = QPixmap(self.main_data.plt_save_path)#.scaled(640, 480)
        self.enh_wav_plt_label.show()
        self.enh_wav_plt_label.setPixmap(jpg)

        self.update_data_pushButton.setEnabled(False)

    def play_wav_file_event(self):
        logger.info("播放原始文件的按钮设置")
        self.play(self.main_data.noisy_wav_path)

    def play_enh_wav_file_event(self):
        logger.info("播放增强文件的按钮设置")
        self.play(self.main_data.enh_wav_path)

    def play(self, filename=None):
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(1024)
        while data != b'':
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
        p.terminate()

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

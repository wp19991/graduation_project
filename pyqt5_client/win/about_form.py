from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import *
from loguru import logger
from ui.about_frame import Ui_Frame as about_frame
import requests


# 自定义信号线程类，一定要继承自 QObject
class get_new_version_thread(QThread):
    # 定义一种信号，两个参数 类型分别是： QProgressBar 和 int
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    nv = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(get_new_version_thread, self).__init__(parent)

    def go(self):
        self.start()

    def run(self):
        try:
            # https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepoReleases
            # TODO 添加修改gitee上传路径
            response = requests.get("https://gitee.com/api/v5/repos/wp19991/speech_enhancement/releases")
            version_information = response.json()
            res = {"status": "ok",
                   "new_version": version_information[-1]["tag_name"],
                   "new_version_function_text": version_information[-1]["body"],
                   "new_version_download_url": "https://gitee.com/wp19991/speech_enhancement"}

            self.nv.emit(res)
        except:
            res = {"status": "error",
                   "new_version": "",
                   "new_version_function_text": "",
                   "new_version_download_url": "https://gitee.com/wp19991/aufe_jwc_app"}
            self.nv.emit(res)


class about_win(QWidget, about_frame):
    def __init__(self, parent=None):
        super(about_win, self).__init__(parent)
        self.setupUi(self)

        self.download_new_version_pushButton.clicked.connect(self.download_new_version_event)

        logger.info("关于软件窗口初始化")
        self.enh_app_update_url = None
        self.now_version_label.setText("0.0.1")

        try:
            # 编写一个函数，返回三个值
            # 创建线程
            self.global_1 = get_new_version_thread()
            # 连接信号
            self.global_1.nv.connect(self.change_nv)
            # 调用线程，进行增强,并且更新进度条
            self.global_1.go()
        except:
            pass

    def change_nv(self, nv_dict):
        if nv_dict["status"] == "ok":
            self.new_version_label.setText(nv_dict["new_version"])
            self.new_version_function_textBrowser.setText(nv_dict["new_version_function_text"])
            self.new_version_download_url = nv_dict["new_version_download_url"]
        else:
            self.new_version_label.setText("网络链接失败")
            self.new_version_download_url = nv_dict["new_version_download_url"]

    def download_new_version_event(self):
        logger.info("下载更新,跳转到网页仓库")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_download_url))

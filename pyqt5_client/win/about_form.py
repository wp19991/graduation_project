from PyQt5.QtWidgets import *
import os
from loguru import logger
from ui.about_frame import Ui_Frame as about_frame


class about_win(QWidget, about_frame):
    def __init__(self, parent=None):
        super(about_win, self).__init__(parent)
        self.setupUi(self)
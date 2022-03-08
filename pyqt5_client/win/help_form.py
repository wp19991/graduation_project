from PyQt5.QtWidgets import *
import os
from loguru import logger
from ui.help_frame import Ui_Frame as help_frame


class help_win(QWidget, help_frame):
    def __init__(self, parent=None):
        super(help_win, self).__init__(parent)
        self.setupUi(self)

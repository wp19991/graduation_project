import sys

from config import config
from myutil import global_var as gl, logs
from PyQt5.QtWidgets import *
from win.main_win import main_win

if __name__ == '__main__':
    gl.__init()
    logs.__init()
    config.__init()
    app = QApplication(sys.argv)
    appWin = main_win()
    appWin.show()
    sys.exit(app.exec_())

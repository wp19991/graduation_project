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

# 转换资源文件
# pyrcc5 apprcc.qrc -o apprcc_rc.py
# 转换ui文件
# python -m PyQt5.uic.pyuic ui/main.ui -o ui/main.py
# 打包成exe
# pyinstaller -F -w -y -i ./resources/icon/探测声音.ico -n 语音增强客户端 main.py

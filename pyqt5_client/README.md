## 毕业设计-客户端-pyqt5

## 介绍

- 输入语音文件
    - 打开文件
    - 输入路径

- 录音
    - 选择录音设备
    - 显示当前录音的大小状态（是否进行录音）

- 进行处理
    - 选择模型
    - 进行处理的按钮
    - 显示处理的进度

- 保存处理好的语音文件
    - 选择输出目录

- 播放语音文件
    - 控制声音大小

- 显示图片plt
    - 显示处理进度
    - 噪音的图片
    - 处理之后的图片

- 显示帮助
    - 显示作者信息
    - 输出帮助文档pdf文件

## 第三方库

```bash
# pyqt5
pip install pyqt5
pip install pyqt5-tools

# 打包程序
pip install pyinstaller

# mysql
pip install pymysql

# ssh
pip install paramiko
```

## Qt Designer 生成 py 文件

```bash
# 转换资源文件
pyrcc5 apprcc.qrc -o apprcc_rc.py

# 转换ui文件
python -m PyQt5.uic.pyuic ui/main.ui -o ui/main.py

# 打包成exe
pyinstaller -F -w -y -i ./ui/icon/images/app.ico -n pyqt5_example main.py
```


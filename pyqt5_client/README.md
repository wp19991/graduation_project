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

## 安装

```bash
conda create -n bysj python=3.8
conda activate bysj
# pyqt5
pip install pyqt5
pip install pyqt5-tools

# 其他
pip install loguru
pip install matplotlib numpy
pip install pyaudio
pip install scipy

# 打包程序
pip install pyinstaller

# mysql
pip install pymysql

# ssh
pip install paramiko


###
pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install librosa soundfile
```

## Qt Designer 生成 py 文件

```bash
# 转换资源文件
pyrcc5 apprcc.qrc -o apprcc_rc.py

# 转换ui文件
python -m PyQt5.uic.pyuic ui/main.ui -o ui/main.py
python -m PyQt5.uic.pyuic ui/sound_recording_frame.ui -o ui/sound_recording_frame.py
python -m PyQt5.uic.pyuic ui/help_frame.ui -o ui/help_frame.py
python -m PyQt5.uic.pyuic ui/about_frame.ui -o ui/about_frame.py

# 打包成exe
#pyinstaller -w -y -i ./resources/icon/探测声音.ico -n 语音增强客户端 main.py
pyinstaller 语音增强客户端.spec
```


# 毕业设计仓库

## 功能介绍

- 输入语音文件
    - [√]打开文件
    - [√]输入路径

- 录音
    - [×]选择录音设备
    - [√]显示当前录音的大小状态（是否进行录音）

- 进行处理
    - [√]切换不同的处理
    - [√]选择模型
    - [√]进行处理的按钮
    - [√]显示处理的进度

- 保存处理好的语音文件
    - [√]选择输出目录

- 播放语音文件
    - [√]播放语音文件
    - [×]控制声音大小

- 显示图片plt
    - [√]显示处理进度
    - [√]噪音的图片
    - [√]处理之后的图片

- 显示帮助
    - [√]显示作者信息
    - [×]输出帮助文档pdf文件

## 安装

```bash
# 创建conda环境
conda create -n bysj python=3.8
# 激活conda环境
conda activate bysj
# 安装各种库
# pyqt5的库
pip install pyqt5
pip install pyqt5-tools
# pytorch
pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
# 其他
pip install librosa
pip install soundfile
pip install loguru
pip install matplotlib
pip install numpy
pip install pyaudio
pip install scipy
pip install pydub
pip install pymysql
pip install paramiko

# 安装打包程序的库
pip install pyinstaller
```

## Qt Designer 生成 py 文件

```bash
# 运行bat文件bulid.bat，记得修改coda环境
# 里面可以进行转换资源文件
# 转换ui文件
```

## 打包

```bash
# 打包成exe
#pyinstaller -w -y -i ./resources/icon/探测声音.ico -n 语音增强客户端 main.py
pyinstaller 语音增强客户端.spec
```

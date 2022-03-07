# 
conda create -n package_pytorch python=3.8
conda activate package_pytorch
pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

pip install librosa soundfile matplotlib

pip install pyinstaller

代码修改成from torch import cat

参考链接：https://blog.csdn.net/u012219045/article/details/113614991

运行
pyinstaller -F use.py

第二行添加
import sys
sys.setrecursionlimit(5000)

在a = Analysis()下面添加
for d in a.datas:
  if '_C.cp38-win_amd64.pyd' in d[0]:
    a.datas.remove(d)
    break

报错:script pyi_rth_win32comgenpy 
解决办法:重装pywin32
需要先将pip降级到9.0（pip install "pip<10"）再进行卸载pywin32
再把pip升级到原版本（pip install pip --upgrade）再安装pywin32
（如果pip没法降的话建议直接上官网找个9.0版本的whl格式或者压缩包进行安装，这样是强制性的安装 anconda阻止不了）

运行
pyinstaller -F use.spec

使用
use.exe --model_file=save/model.pkl --noisy_file=wav/p232_010.wav --save_path=ss

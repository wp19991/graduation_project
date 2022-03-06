import os
import torch
import torch.nn as nn
import librosa
import numpy as np

import soundfile as sf
import matplotlib.pyplot as plt


class Generator(nn.Module):
    """G"""

    def __init__(self):
        super().__init__()
        # encoder gets a noisy signal as input [B x 1 x 16384]
        self.enc1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=32, stride=2, padding=15)  # [B x 16 x 8192]
        self.enc1_nl = nn.PReLU()
        self.enc2 = nn.Conv1d(16, 32, 32, 2, 15)  # [B x 32 x 4096]
        self.enc2_nl = nn.PReLU()
        self.enc3 = nn.Conv1d(32, 32, 32, 2, 15)  # [B x 32 x 2048]
        self.enc3_nl = nn.PReLU()
        self.enc4 = nn.Conv1d(32, 64, 32, 2, 15)  # [B x 64 x 1024]
        self.enc4_nl = nn.PReLU()
        self.enc5 = nn.Conv1d(64, 64, 32, 2, 15)  # [B x 64 x 512]
        self.enc5_nl = nn.PReLU()
        self.enc6 = nn.Conv1d(64, 128, 32, 2, 15)  # [B x 128 x 256]
        self.enc6_nl = nn.PReLU()
        self.enc7 = nn.Conv1d(128, 128, 32, 2, 15)  # [B x 128 x 128]
        self.enc7_nl = nn.PReLU()
        self.enc8 = nn.Conv1d(128, 256, 32, 2, 15)  # [B x 256 x 64]
        self.enc8_nl = nn.PReLU()
        self.enc9 = nn.Conv1d(256, 256, 32, 2, 15)  # [B x 256 x 32]
        self.enc9_nl = nn.PReLU()
        self.enc10 = nn.Conv1d(256, 512, 32, 2, 15)  # [B x 512 x 16]
        self.enc10_nl = nn.PReLU()
        self.enc11 = nn.Conv1d(512, 1024, 32, 2, 15)  # [B x 1024 x 8]
        self.enc11_nl = nn.PReLU()

        # decoder generates an enhanced signal
        # each decoder output are concatenated with homologous encoder output,
        # so the feature map sizes are doubled
        self.dec10 = nn.ConvTranspose1d(in_channels=2048, out_channels=512, kernel_size=32, stride=2, padding=15)
        self.dec10_nl = nn.PReLU()  # out : [B x 512 x 16] -> (concat) [B x 1024 x 16]
        self.dec9 = nn.ConvTranspose1d(1024, 256, 32, 2, 15)  # [B x 256 x 32]
        self.dec9_nl = nn.PReLU()
        self.dec8 = nn.ConvTranspose1d(512, 256, 32, 2, 15)  # [B x 256 x 64]
        self.dec8_nl = nn.PReLU()
        self.dec7 = nn.ConvTranspose1d(512, 128, 32, 2, 15)  # [B x 128 x 128]
        self.dec7_nl = nn.PReLU()
        self.dec6 = nn.ConvTranspose1d(256, 128, 32, 2, 15)  # [B x 128 x 256]
        self.dec6_nl = nn.PReLU()
        self.dec5 = nn.ConvTranspose1d(256, 64, 32, 2, 15)  # [B x 64 x 512]
        self.dec5_nl = nn.PReLU()
        self.dec4 = nn.ConvTranspose1d(128, 64, 32, 2, 15)  # [B x 64 x 1024]
        self.dec4_nl = nn.PReLU()
        self.dec3 = nn.ConvTranspose1d(128, 32, 32, 2, 15)  # [B x 32 x 2048]
        self.dec3_nl = nn.PReLU()
        self.dec2 = nn.ConvTranspose1d(64, 32, 32, 2, 15)  # [B x 32 x 4096]
        self.dec2_nl = nn.PReLU()
        self.dec1 = nn.ConvTranspose1d(64, 16, 32, 2, 15)  # [B x 16 x 8192]
        self.dec1_nl = nn.PReLU()
        self.dec_final = nn.ConvTranspose1d(32, 1, 32, 2, 15)  # [B x 1 x 16384]
        self.dec_tanh = nn.Tanh()

        # initialize weights
        self.init_weights()

    def init_weights(self):
        """
        Initialize weights for convolution layers using Xavier initialization.
        """
        for m in self.modules():
            if isinstance(m, nn.Conv1d) or isinstance(m, nn.ConvTranspose1d):
                nn.init.xavier_normal(m.weight.data)

    def forward(self, x, z):
        """
        Forward pass of generator.

        Args:
            x: input batch (signal)
            z: latent vector
        """
        # encoding step
        e1 = self.enc1(x)
        e2 = self.enc2(self.enc1_nl(e1))
        e3 = self.enc3(self.enc2_nl(e2))
        e4 = self.enc4(self.enc3_nl(e3))
        e5 = self.enc5(self.enc4_nl(e4))
        e6 = self.enc6(self.enc5_nl(e5))
        e7 = self.enc7(self.enc6_nl(e6))
        e8 = self.enc8(self.enc7_nl(e7))
        e9 = self.enc9(self.enc8_nl(e8))
        e10 = self.enc10(self.enc9_nl(e9))
        e11 = self.enc11(self.enc10_nl(e10))
        # c = compressed feature, the 'thought vector'
        c = self.enc11_nl(e11)

        # concatenate the thought vector with latent variable
        encoded = torch.cat((c, z), dim=1)

        # decoding step
        d10 = self.dec10(encoded)
        # dx_c : concatenated with skip-connected layer's output & passed nonlinear layer
        d10_c = self.dec10_nl(torch.cat((d10, e10), dim=1))
        d9 = self.dec9(d10_c)
        d9_c = self.dec9_nl(torch.cat((d9, e9), dim=1))
        d8 = self.dec8(d9_c)
        d8_c = self.dec8_nl(torch.cat((d8, e8), dim=1))
        d7 = self.dec7(d8_c)
        d7_c = self.dec7_nl(torch.cat((d7, e7), dim=1))
        d6 = self.dec6(d7_c)
        d6_c = self.dec6_nl(torch.cat((d6, e6), dim=1))
        d5 = self.dec5(d6_c)
        d5_c = self.dec5_nl(torch.cat((d5, e5), dim=1))
        d4 = self.dec4(d5_c)
        d4_c = self.dec4_nl(torch.cat((d4, e4), dim=1))
        d3 = self.dec3(d4_c)
        d3_c = self.dec3_nl(torch.cat((d3, e3), dim=1))
        d2 = self.dec2(d3_c)
        d2_c = self.dec2_nl(torch.cat((d2, e2), dim=1))
        d1 = self.dec1(d2_c)
        d1_c = self.dec1_nl(torch.cat((d1, e1), dim=1))
        out = self.dec_tanh(self.dec_final(d1_c))
        return out


def emphasis(signal, emph_coeff=0.95, pre=True):
    if pre:
        result = np.append(signal[0], signal[1:] - emph_coeff * signal[:-1])
    else:
        result = np.append(signal[0], signal[1:] + emph_coeff * signal[:-1])

    return result


def enh_segan(model, noisy):
    # 对输入的noisy 按照 win_len 进行分段，没有重叠

    win_len = 16384
    # 不足的部分 重复填充
    N_slice = len(noisy) // win_len
    temp_noisy = None
    if not len(noisy) % win_len == 0:
        short = win_len - len(noisy) % win_len
        temp_noisy = np.pad(noisy, (0, short), 'wrap')
        N_slice = N_slice + 1

    slices = temp_noisy.reshape(N_slice, win_len)

    enh_slice = np.zeros(slices.shape)

    # 逐帧进行处理
    for n in range(N_slice):
        m_slice = slices[n]

        # 进行预加重
        m_slice = emphasis(m_slice)
        # 增加 2个维度
        m_slice = np.expand_dims(m_slice, axis=(0, 1))
        # 转换为torch格式

        m_slice = torch.from_numpy(m_slice)

        # 生成 z
        z = nn.init.normal_(torch.Tensor(1, 1024, 8))

        # 进行增强
        model.eval()
        with torch.no_grad():
            print("m_slice.shape", m_slice.shape)
            print("z.shape", z.shape)
            generated_slice = model(m_slice, z)
            print("generated_slice.shape", generated_slice.shape)
        generated_slice = generated_slice.numpy()
        # 反预加重
        generated_slice = emphasis(generated_slice[0, 0, :], pre=False)
        enh_slice[n] = generated_slice

    # 信号展开
    enh_speech = enh_slice.reshape(N_slice * win_len)
    return enh_speech[:len(noisy)]

def get_and_save_enh(model_file,noisy_file_path,save_path):
	os.makedirs(save_path,exist_ok=True)
    generator = Generator()
    generator.load_state_dict(torch.load(model_file, map_location='cpu'))
    noisy, _ = librosa.load(noisy_file_path, sr=16000, mono=True)

    # 获取增强语音
    enh = enh_segan(generator, noisy)

    # 语音保存
    sf.write(os.path.join(save_path, 'noisy-' + os.path.split(noisy_file_path)[-1]), noisy, 16000)
    sf.write(os.path.join(save_path, 'enh-' + os.path.split(noisy_file_path)[-1]), enh, 16000)

    # 画频谱图
    # 绘图
    fig_name = os.path.join(save_path, os.path.split(noisy_file_path)[-1][:-4] + '.jpg')


    # 其中各个参数也可以用逗号,分隔开。第一个参数代表子图的行数；第二个参数代表该行图像的列数； 第三个参数代表每行的第几个图像。
    # 2代表行，1代表列，所以一共有2个图，1代表此时绘制第二个图。其中ax1是为了坐标轴主次刻度大小的设置
    plt.subplot(2, 1, 1)
    plt.specgram(noisy, NFFT=512, Fs=16000)
    plt.xlabel("noisy specgram")
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0, hspace=0.5)

    plt.subplot(2, 1, 2)
    plt.specgram(enh, NFFT=512, Fs=16000)
    plt.xlabel("enhece specgram")
    plt.savefig(fig_name)
    pass


if __name__ == "__main__":
    model_file = "save/G_5_0.3193.pkl"
    noisy_file_path = './wav/p232_010.wav'
    save_path = "ssss"
    get_and_save_enh(model_file, noisy_file_path, save_path)








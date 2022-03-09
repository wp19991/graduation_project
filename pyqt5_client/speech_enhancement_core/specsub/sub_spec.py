import librosa
import numpy as np
import os
import soundfile as sf
import matplotlib.pyplot as plt


class specsub:
    def __init__(self, noisy_wav_file_path, alpha=4, gamma=1, beta=0.0001, k=1):
        if not os.path.exists(noisy_wav_file_path):
            a = 1 / 0
        self.noisy_wav_file_path = noisy_wav_file_path
        self.alpha = alpha
        self.gamma = gamma
        self.beta = beta
        self.k = k

        self.noisy, self.fs = librosa.load(self.noisy_wav_file_path, sr=None)
        self.enhance = None

        self.is_fit = False

    def fit(self):
        # 计算 nosiy 信号的频谱
        S_noisy = librosa.stft(self.noisy, n_fft=256, hop_length=128, win_length=256)  # D x T
        D, T = np.shape(S_noisy)
        Mag_noisy = np.abs(S_noisy)
        Phase_nosiy = np.angle(S_noisy)
        # 估计噪声信号的能量
        # 由于噪声信号未知 这里假设 含噪（noisy）信号的前30帧为噪声
        Mag_nosie = np.mean(np.abs(S_noisy[:, :31]), axis=1, keepdims=True)
        Power_nosie = Mag_nosie ** 2
        Power_nosie = np.tile(Power_nosie, [1, T])
        ## 引入平滑
        Mag_noisy_new = np.copy(Mag_noisy)
        for t in range(self.k, T - self.k):
            Mag_noisy_new[:, t] = np.mean(Mag_noisy[:, t - self.k:t + self.k + 1], axis=1)
        Power_nosiy = Mag_noisy_new ** 2
        # 超减法去噪
        Power_enhenc = np.power(Power_nosiy, self.gamma) - self.alpha * np.power(Power_nosie, self.gamma)
        Power_enhenc = np.power(Power_enhenc, 1 / self.gamma)
        # 对于过小的值用 beta* Power_nosie 替代
        mask = (Power_enhenc >= self.beta * Power_nosie) - 0
        Power_enhenc = mask * Power_enhenc + self.beta * (1 - mask) * Power_nosie
        Mag_enhenc = np.sqrt(Power_enhenc)
        Mag_enhenc_new = np.copy(Mag_enhenc)
        # 计算最大噪声残差
        maxnr = np.max(np.abs(S_noisy[:, :31]) - Mag_nosie, axis=1)
        for t in range(self.k, T - self.k):
            index = np.where(Mag_enhenc[:, t] < maxnr)[0]
            temp = np.min(Mag_enhenc[:, t - self.k:t + self.k + 1], axis=1)
            Mag_enhenc_new[index, t] = temp[index]
        # 对信号进行恢复
        S_enhance = Mag_enhenc_new * np.exp(1j * Phase_nosiy)
        self.enhance = librosa.istft(S_enhance, hop_length=128, win_length=256)
        self.is_fit = True

    def output_file(self, wav_file_output_path=os.getcwd(), name=None):
        if name is None:
            name = os.path.basename(self.noisy_wav_file_path) + "_sub_spec_enhance.wav"
        opp = os.path.join(wav_file_output_path, name)
        sf.write(opp, self.enhance, self.fs)
        return name

    def plt_save(self,output_path=os.getcwd()):
        # 绘制噪音的谱图
        plt.subplot(3, 1, 1)
        plt.specgram(self.noisy, NFFT=512, Fs=16000)
        plt.xlabel("before specgram")
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=0, hspace=0.8)

        plt.subplot(3, 1, 2)
        plt.specgram(self.noisy - self.enhance, NFFT=512, Fs=16000)
        plt.xlabel("background noisy specgram")
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=0, hspace=0.8)

        plt.subplot(3, 1, 3)
        plt.specgram(self.enhance, NFFT=512, Fs=16000)
        plt.xlabel("enhece after specgram")
        opp = os.path.join(output_path,
                           "noisy_sub_spec_specgram_" + os.path.basename(self.noisy_wav_file_path) + ".png")
        plt.savefig(opp)


if __name__ == "__main__":
    a = specsub(noisy_wav_file_path=r"C:\Users\wp\Desktop\graduation_project\specsub\noise_wav\speech-us-gov-0000.wav")
    a.fit()
    a.plt_save(output_path=r"C:\Users\wp\Desktop\graduation_project\output")
    a.output_file(wav_file_output_path=r"C:\Users\wp\Desktop\graduation_project\output")

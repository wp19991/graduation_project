import os
from torch import cat
from torch import from_numpy
from torch import Tensor
from torch import no_grad
from torch import load

from torch import nn

from librosa import load as librosa_load
import numpy as np

import soundfile as sf


class Generator(nn.Module):
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
                nn.init.xavier_normal_(m.weight.data)

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
        encoded = cat((c, z), dim=1)

        # decoding step
        d10 = self.dec10(encoded)
        # dx_c : concatenated with skip-connected layer's output & passed nonlinear layer
        d10_c = self.dec10_nl(cat((d10, e10), dim=1))
        d9 = self.dec9(d10_c)
        d9_c = self.dec9_nl(cat((d9, e9), dim=1))
        d8 = self.dec8(d9_c)
        d8_c = self.dec8_nl(cat((d8, e8), dim=1))
        d7 = self.dec7(d8_c)
        d7_c = self.dec7_nl(cat((d7, e7), dim=1))
        d6 = self.dec6(d7_c)
        d6_c = self.dec6_nl(cat((d6, e6), dim=1))
        d5 = self.dec5(d6_c)
        d5_c = self.dec5_nl(cat((d5, e5), dim=1))
        d4 = self.dec4(d5_c)
        d4_c = self.dec4_nl(cat((d4, e4), dim=1))
        d3 = self.dec3(d4_c)
        d3_c = self.dec3_nl(cat((d3, e3), dim=1))
        d2 = self.dec2(d3_c)
        d2_c = self.dec2_nl(cat((d2, e2), dim=1))
        d1 = self.dec1(d2_c)
        d1_c = self.dec1_nl(cat((d1, e1), dim=1))
        out = self.dec_tanh(self.dec_final(d1_c))
        return out


def emphasis(signal, emph_coeff=0.95, pre=True):
    if pre:
        result = np.append(signal[0], signal[1:] - emph_coeff * signal[:-1])
    else:
        result = np.append(signal[0], signal[1:] + emph_coeff * signal[:-1])

    return result


def enh_segan(model, noisy):
    # ????????????noisy ?????? win_len ???????????????????????????
    win_len = 16384
    # ??????????????? ????????????
    N_slice = len(noisy) // win_len
    temp_noisy = None
    if not len(noisy) % win_len == 0:
        short = win_len - len(noisy) % win_len
        temp_noisy = np.pad(noisy, (0, short), 'wrap')
        N_slice = N_slice + 1

    slices = temp_noisy.reshape(N_slice, win_len)

    enh_slice = np.zeros(slices.shape)

    # ??????????????????
    for n in range(N_slice):
        m_slice = slices[n]

        # ???????????????
        m_slice = emphasis(m_slice)
        # ?????? 2?????????
        m_slice = np.expand_dims(m_slice, axis=(0, 1))
        # ?????????torch??????

        m_slice = from_numpy(m_slice)

        # ?????? z
        z = nn.init.normal_(Tensor(1, 1024, 8))

        # ????????????
        model.eval()
        with no_grad():
            generated_slice = model(m_slice, z)
        generated_slice = generated_slice.numpy()
        # ????????????
        generated_slice = emphasis(generated_slice[0, 0, :], pre=False)
        enh_slice[n] = generated_slice

    # ????????????
    enh_speech = enh_slice.reshape(N_slice * win_len)
    return enh_speech[:len(noisy)]


def get_and_save_enh(model_file, noisy_file, output_path=os.getcwd()):
    os.makedirs(output_path, exist_ok=True)
    generator = Generator()
    generator.load_state_dict(load(model_file, map_location='cpu'))
    noisy, _ = librosa_load(noisy_file, sr=16000, mono=True)

    # ??????????????????
    enh = enh_segan(generator, noisy)

    name = "noisy_SEGAN_enhance_" + os.path.basename(noisy_file)
    enh_wav_path = output_path + "/" + name
    sf.write(enh_wav_path, enh, 16000)

    return enh_wav_path


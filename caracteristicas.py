import pywt
import numpy as np
from scipy.fft import rfft, rfftfreq

# Calcula características estadísticas en el dominio del tiempo
def extraer_tiempo(instancia):
    rms = np.sqrt(np.mean(instancia**2, axis=0))
    mav = np.mean(np.abs(instancia), axis=0)
    zc = np.sum(np.diff(np.sign(instancia), axis=0) != 0, axis=0)
    return np.concatenate([rms, mav, zc])

# FFT y cálculo de frecuencia media/mediana
def extraer_frecuencia(instancia, fs=200):
    n = instancia.shape[0]
    freqs = rfftfreq(n, 1/fs)
    fft_vals = np.abs(rfft(instancia, axis=0))
    mnf = np.sum(freqs[:, None] * fft_vals, axis=0) / np.sum(fft_vals, axis=0)
    return mnf

# Energía por nivel
def extraer_dwt(instancia, wave='db4', nivel=4):
    coeffs = pywt.wavedec(instancia, wave, level=nivel)
    return np.concatenate([np.sum(c**2, axis=0) for c in coeffs])

# Enerfia por escala
def extraer_cwt(instancia, scales=np.arange(1, 65), wave='cmor'):
    # Canal 1 solamente para escalograma 
    coeffs, _ = pywt.cwt(instancia[:, 0], scales, wave)
    return np.sum(np.abs(coeffs)**2, axis=1)
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import wave
from pylab import *

fn = r"test.wav"

with wave.open(fn, 'r') as wfin, wave.open('filtered-talk.wav', 'w') as wfout:  # Открытие файлов
    par = list(wfin.getparams())  # Получение параметров из файла.
    par[3] = 0  # Убираем неиспользуемые для сжатия параметры
    wfout.setparams(tuple(par))  # применяем параметры входного файла к output-файлу
    lowpass, highpass = 21, 9000  # ограничиваем частоты

    sz = wfin.getframerate()  # получаем герцовку аудио
    c = int(wfin.getnframes() / sz)  # делим весь файл на звуковые фрагменты
    for num in range(c):
        print('Processing {}/{} s'.format(num + 1, c))
        da = np.fromstring(wfin.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2]  # левый и правый каналы
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf[:lowpass], rf[:lowpass] = 0, 0  # фильтруем нижние частоты
        lf[55:66], rf[55:66] = 0, 0  # убираем линейный шум
        lf[highpass:], rf[highpass:] = 0, 0  # фильтруем верхние частоты
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
        wfout.writeframes(ns.tostring())

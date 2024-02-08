import numpy as np
import soundfile as sf
from pydub import AudioSegment


def f(wav_file="source_file.wav", wav_compressed_file="audio_compressed.wav"):
    # Конвертировать wav в mp3
    audio = AudioSegment.from_wav(wav_file)
    # audio.export(wav_file, format="wav")
    # Получить данные из wav-файла
    data, samplerate = sf.read(wav_file)
    n = len(data)  # длина массивов, содержащихся в данных
    fs = samplerate  # частота дискретизации
    # При работе со стереозвуком в аудиоданных имеется два канала.
    # Давайте извлечем каждый канал отдельно:
    ch1 = np.array([data[i][0] for i in range(n)])  # канал 1
    ch2 = np.array([data[i][1] for i in range(n)])  # канал 2
    ch1_fourier = np.fft.fft(ch1)  # выполнение быстрого преобразования Фурье
    abs_ch1_fourier = np.absolute(ch1_fourier[:n // 2])  # спектр
    eps = 1e-5
    # Логический массив, где каждое значение указывает, сохраняем ли мы соответствующую частоту.
    frequencies_to_remove = (1 - eps) * np.sum(abs_ch1_fourier) < np.cumsum(abs_ch1_fourier)
    # Частота, на которую мы обрезаем спектр
    f0 = (len(frequencies_to_remove) - np.sum(frequencies_to_remove)) * (fs / 2) / (n / 2)
    d = int(fs / f0)  # Затем мы определяем коэффициент понижающей дискретизации
    new_data = data[::d, :]  # получение уменьшенных данных
    # Запись новых данных в wav-файл
    sf.write(wav_compressed_file, new_data, int(fs / d), 'PCM_U8')
    audio_сompressed = AudioSegment.from_wav(wav_compressed_file)
    audio_сompressed.export(wav_compressed_file, format="wav")


f("source_file.wav", "audio_compressed1.wav")
f("audio_compressed1.wav", "audio_compressed2.wav")
f("audio_compressed2.wav", "audio_compressed3.wav")
f("audio_compressed3.wav", "audio_compressed4.wav")
f("audio_compressed4.wav", "audio_compressed5.wav")

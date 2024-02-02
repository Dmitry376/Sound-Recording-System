import wave
from pydub import AudioSegment

input_file = wave.open('test.wav', 'rb')  # открываем файлы на чтение и запись
out_file = wave.open('result.wav', 'wb')
frames = []
for i in range(input_file.getnframes()):
    frames.append(input_file.readframes(i))  # собираем аудио фрагменты из исходного файла
out_file.setnchannels(
    1)  # задаем параметры(кол-во каналов: моно, стерео;глубина звука и герцовка). Они влияют на качество звука
out_file.setsampwidth(4)
out_file.setframerate(24000)
for i in range(len(frames)):
    out_file.writeframes(frames[i])  # запись собранных фрагментов в новый файл

root = r'result.wav'  # ускорение аудио (при уменьшении параметров аудио может увеличится длина из-за потери качества)
pace = 1.5

sound = AudioSegment.from_file(root)
sound = sound.speedup(pace, chunk_size=150, crossfade=0)
sound.export(root, format='wav')  # сохраняем файл

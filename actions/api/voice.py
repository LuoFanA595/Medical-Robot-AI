# -*- codeing = utf-8 -*-
# @Time :2021/8/20 15:51
# @Author : 兢兢业业的小码农
# @File : voice.py
# @Software : PyCharm
# @Email: 1795947368@qq.com

from aip import AipSpeech
import pyaudio
import wave

""" 你的 APPID AK SK """
APP_ID = '24728390'
API_KEY = 'd4xMCdaKuk0qMaOZjEkUF2x2'
SECRET_KEY = 'HP41TguxWiNEtWIxtBgYbblm4WNVgYGw'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

'''读取音频文件'''


def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()


'''语音采集部分'''


def get_audio(filepath):
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # 声道数
    RATE = 11025  # 采样率
    RECORD_SECONDS = 5  # 采集时间（s）
    WAVE_OUTPUT_FILENAME = filepath  # 输出文件名和路径
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*" * 10, "开始录音：请在5秒内输入语音")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*" * 10, "录音结束\n")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def main(in_path):
    for i in range(1):
        get_audio(in_path)
        # 语音识别
        keyword = client.asr(get_file_content(in_path), 'pcm', 16000,
                             {'dev_ped': 1537})
        return keyword['result'][0]

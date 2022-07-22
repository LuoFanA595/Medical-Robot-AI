# -*- codeing = utf-8 -*-

import pyttsx3
from pyttsx3.voice import Voice
def yuyin(hua):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')

    # 控制语音播放的速度
    engine.setProperty('rate', 180)
    volume = engine.getProperty('volume')

    # 控制语音播放的音量大小
    engine.setProperty('volume',0)
    voice = engine.getProperty('voice')

    v = Voice(id=1, name='财神', languages='Japanese', age=18, gender='女')
    engine.setProperty('voice', v)
    engine.say(hua)
    engine.runAndWait()    #朗读一次

if __name__ == '__main__':
    yuyin('')

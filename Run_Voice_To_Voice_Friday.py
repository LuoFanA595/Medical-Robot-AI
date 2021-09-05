import json
import secrets
import requests
from actions.api import voice
import asyncio
import yaml
from rasa.core.agent import Agent
from rasa.shared.constants import DEFAULT_ENDPOINTS_PATH
from rasa.utils.endpoints import EndpointConfig
import pyttsx3
from pyttsx3.voice import Voice

url = "http://localhost:5005/webhooks/rest/webhook"
in_path = r"录音文件\input.wav"

# 需要先训练好一个模型
with open(DEFAULT_ENDPOINTS_PATH) as fp:
    endpoint = EndpointConfig.from_dict(yaml.load(fp).get("action_endpoint"))

agent = Agent.load_local_model(
    model_path="models",
    action_endpoint=endpoint
)


def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r


def textToAudio(message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')

    # 控制语音播放的速度
    engine.setProperty('rate', 180)
    volume = engine.getProperty('volume')

    # 控制语音播放的音量大小
    engine.setProperty('volume', 0.9)
    voice = engine.getProperty('voice'
                               '')

    v = Voice(id=1, name='Friday', languages='chinese', age=18, gender='女')
    engine.setProperty('voice', v)
    engine.say(message)
    engine.runAndWait()  # 朗读一次


sender = secrets.token_urlsafe(16)

while True:
    message = voice.main(in_path)
    print('Your>>>', message)
    for line in asyncio.get_event_loop().run_until_complete(agent.handle_text(message)):
        print('Friday>>>', line['text'])
        textToAudio(line['text'])

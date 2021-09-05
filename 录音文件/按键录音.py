from pynput import keyboard
import time
import pyaudio
import wave
import sched
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = r"/录音文件/input.wav"

p = pyaudio.PyAudio()
frames = []

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
     super(MyListener, self).__init__(self.on_press, self.on_release)
     self.key_pressed = None
     self.wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
     self.wf.setnchannels(CHANNELS)
     self.wf.setsampwidth(p.get_sample_size(FORMAT))
     self.wf.setframerate(RATE)
    def on_press(self, key):
     if key.char == 'r':
      self.key_pressed = True
     return True

    def on_release(self, key):
     if key.char == 'r':
      self.key_pressed = False
     return True


listener = MyListener()
listener.start()
started = False
stream = None

def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
     # Start the recording
     try:
      stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK,
          stream_callback = callback)
      print("流活跃:", stream.is_active())
      started = True
      print("开始流")
     except:
      raise

    elif not listener.key_pressed and started:
     print("停止录音")
     stream.stop_stream()
     stream.close()
     p.terminate()
     listener.wf.writeframes(b''.join(frames))
     listener.wf.close()
     print("您应该在当前目录中有一个 wav 文件")
     sys.exit()
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder,())


print("按住“r”键开始录音")
print("松开“r”键结束录音")
task = sched.scheduler(time.time, time.sleep)
task.enter(0.1, 1, recorder,())
task.run()
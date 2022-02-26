import pyaudio
import wave
from aip import AipSpeech
import os
from xpinyin import Pinyin


APP_ID='23084370'
API_KEY='KpNbsHjl3BPsKGXgc6r9bbzt'
SECRET_KEY='RyqDNA3ACZB857kLxM7VHCGZxGk4HylB'

client=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream.start_stream()
print("* 开始录音......")

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

with open('audio.wav', 'rb') as fp:
        wave=fp.read()

print("* 正在识别......",len(wave))
result = client.asr(wave, 'wav', 16000, {'dev_pid':1537})
print(result)
if result["err_no"] == 0:
    for t in result["result"]:
        print(t)
else:
    print("没有识别到语音\n",result["err_no"])



p=Pinyin()
ptxt=p.get_pinyin(result["result"][0])
print(ptxt)
if "ma-po-dou-fu" in ptxt:
    voice=client.synthesis("好的，你要几碗？",'zh',6,{'vol':15,'per':4,'spd':5})
    with open("playback.mp3",'wb') as fp:
        fp.write(voice)
    os.system("playback.mp3")
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 8000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stream.start_stream()
    print("* 开始录音......")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    with open('audio.wav', 'rb') as fp:
            wave=fp.read()

    print("* 正在识别......",len(wave))
    result = client.asr(wave, 'wav', 16000, {'dev_pid':1537})
    print(result)
    if result["err_no"] == 0:
        for t in result["result"]:
            print(t)
    else:
        print("没有识别到语音\n",result["err_no"])



    p=Pinyin()
    ptxt=p.get_pinyin(result["result"][0])
    print(ptxt)
    if "3-wan" in ptxt:
        voice=client.synthesis("一共200元",'zh',6,{'vol':15,'per':4,'spd':5})
    with open("playback.mp3",'wb') as fp:
        fp.write(voice)
    os.system("playback.mp3")




    

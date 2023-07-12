import pyaudio
import wave
import os
import numpy as np
import datetime


def get_devices():
    p = pyaudio.PyAudio()
    devices = []
    device2index_map = dict()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info["name"]
        if ("input" in device_name)|("Input" in device_name)|("()" in device_name):
            continue
        devices.append(device_name)
        device2index_map.update({device_name: device_info["index"]})

    p.terminate()

    return devices, device2index_map

def record_voice(directory, device_index=0):
    threshold = 0.03
    thresholdmin = 0.02
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    blank = 1
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=chunk,
        input_device_index=device_index
        )
    sound=[]
    os.makedirs(f"{directory}{os.sep}tmp", exist_ok=True)
    
    while True:
        data = stream.read(chunk)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        if x.max() > threshold:
            rec = 0
            datetime_now = datetime.datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")
            filename = f"{directory}{os.sep}tmp{os.sep}voice_{datetime_now}.wav"
            sound=[]
            sound.append(data)
            while rec < int(blank * RATE / chunk):
                data = stream.read(chunk)

                sound.append(data)
                x = np.frombuffer(data, dtype="int16") / 32768.0
                if x.max() < thresholdmin:
                    rec += 1
                else:
                    rec = 0

            data = b''.join(sound)

            out = wave.open(filename,'w')
            out.setnchannels(CHANNELS)
            out.setsampwidth(2)
            out.setframerate(RATE)
            out.writeframes(data)
            out.close()

            break

    stream.close()
    p.terminate()

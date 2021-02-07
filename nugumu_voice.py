# coding: utf-8
import win32com.client as wincl
import wave
import os
from winsound import PlaySound, SND_MEMORY
import PySimpleGUI as psg


def nugumu_speak(text):
    os.makedirs("tmp", exist_ok=True)
    voice = wincl.Dispatch("SAPI.SpVoice")
    savefile = wincl.Dispatch("SAPI.SpFileStream")
    voice.Rate = -6
    pitch = -10
    sentence = f'<pitch absmiddle=\"{pitch}\">{text}</pitch>'

    savefile.Open("tmp/normal.wav", 3)
    voice.AudioOutputStream = savefile
    voice.Speak(sentence)
    savefile.Close()

    change_rate = 0.8
    with wave.open("tmp/normal.wav", "rb") as voicefile:
        rate = voicefile.getframerate()
        signal = voicefile.readframes(-1)
    with wave.open("tmp/adjusted.wav", "wb") as adjusted_voicefile:
        adjusted_voicefile.setnchannels(1)
        adjusted_voicefile.setsampwidth(2)
        adjusted_voicefile.setframerate(rate*change_rate)
        adjusted_voicefile.writeframes(signal)

    with open("tmp/adjusted.wav", "rb") as f:
        data = f.read()

    PlaySound(data, SND_MEMORY)
    
psg.theme("Dark Red 2")

layout = [
    [psg.Text("險?闡", size=(15, 1)), psg.InputText("")],
    [psg.Submit(button_text="蜃ｺ蜉")]
]

window = psg.Window("遘縺励縺ｹ繧翫縺", layout)

while True:
    event, values = window.read()

    if event is None:
        print("邨ゆｺ?縺ｾ縺励")
        break

    if event == "蜃ｺ蜉":
        print(values[0])
        nugumu_speak(values[0])

window.close()

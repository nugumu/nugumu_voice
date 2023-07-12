import win32com.client as wincl
import wave
import os
from winsound import PlaySound, SND_MEMORY


def nugumu_speak(text, directory):
    os.makedirs(f"{directory}{os.sep}tmp", exist_ok=True)
    voice = wincl.Dispatch("SAPI.SpVoice")
    savefile = wincl.Dispatch("SAPI.SpFileStream")
    voice.Rate = -6
    pitch = -10
    sentence = f'<pitch absmiddle=\"{pitch}\">{text}</pitch>'
    normal_voice_savepath = f"{directory}{os.sep}tmp{os.sep}normal.wav"
    adjusted_voice_savepath = f"{directory}{os.sep}tmp{os.sep}adjusted.wav"
    print(f"save nomal voice to {normal_voice_savepath}")
    savefile.Open(normal_voice_savepath, 3)
    voice.AudioOutputStream = savefile
    voice.Speak(sentence)
    savefile.Close()

    change_rate = 0.8
    with wave.open(normal_voice_savepath, "rb") as voicefile:
        rate = voicefile.getframerate()
        signal = voicefile.readframes(-1)
    
    print(f"save adjusted voice to {adjusted_voice_savepath}")
    with wave.open(adjusted_voice_savepath, "wb") as adjusted_voicefile:
        adjusted_voicefile.setnchannels(1)
        adjusted_voicefile.setsampwidth(2)
        adjusted_voicefile.setframerate(rate*change_rate)
        adjusted_voicefile.writeframes(signal)

    with open(f"{directory}{os.sep}tmp{os.sep}adjusted.wav", "rb") as f:
        data = f.read()

    PlaySound(data, SND_MEMORY)

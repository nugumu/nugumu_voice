import speech_recognition as sr
import os
import glob


def voice2text(directory):
    recognizer = sr.Recognizer()
    files = glob.glob(f"{directory}{os.sep}tmp{os.sep}voice*.wav")
    files.sort(key=lambda x: int(os.path.getctime(x)), reverse=True)
    filepath = files[0]
    print(f"load voice from {filepath}")
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio, language="ja-JP")

    return text

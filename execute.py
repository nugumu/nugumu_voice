import PySimpleGUI as psg
import os
import traceback
from recordvoice import record_voice, get_devices
from voice2text import voice2text


psg.theme("Dark Red 2")
# Windows でなければ警告
if os.name == "nt":
    from nugumuvoice import nugumu_speak
else:
    psg.popup_ok("このアプリケーションは Windows 専用です。", title="警告")

# デバイスを読み込む
devices, device2index_map = get_devices()
# カレントディレクトリを読み込む
directory = os.getcwd()
print(directory)

# 入力窓
layout = [
    [psg.InputText(""), psg.Submit(button_text="文字入力")],
    [psg.Combo(devices, default_value="音声入力デバイスを選択してください。"), psg.Submit(button_text="音声入力")],
    [psg.Submit(button_text="終了")]
]
window = psg.Window("ンヌグムおしゃべり", layout)

while True:
    event, values = window.read()
    device_name = values[1]

    try:
        if event == "終了":
            window.close()

        if event == "文字入力":
            text = values[0]
            print(f"input text: {text}")
            # ンヌグムの声で再生
            nugumu_speak(text, directory=directory)

        if event == "音声入力":
            # 入力デバイスを選択
            if device_name in device2index_map.keys():
                device_index = device2index_map[device_name]
            else:
                device_index = 0
            # 録音
            record_voice(directory=directory, device_index=device_index)
            # 文字起こし
            text = voice2text(directory=directory)
            print(f"input text: {text}")
            # ンヌグムの声で再生
            nugumu_speak(text, directory=directory)

    except:
        error = traceback.format_exc()
        psg.popup_ok("エラー内容：", error, title="エラー発生")

window.close()

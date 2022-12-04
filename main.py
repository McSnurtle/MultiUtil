# imports
import playsound
from art import tprint
from tkinter import Tk
from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
from pynput.keyboard import Key, Controller
from time import sleep
from winsound import PlaySound, SND_ASYNC
import os
from sys import exit


tprint("GAME UTILS", font="qwertyui")
print("")
print("-------------------------------------------------------------------------------------------------------------------")
print("COMMANDS:")
print("Enter 'voice' to start and focus voice tools\n"
      "Enter 'blk-screen' to start and focus a black screen\n"
      "Thanks for using GAME UTILS!~\n"
      "\n"
      "By Mc_Snurtle")
print("-------------------------------------------------------------------------------------------------------------------")
print("")


def simulate_string(string, delay):
    string = str(string).split("type ")
    for char in string[1]:
        keyboard.press(char)
        keyboard.release(char)
        sleep(delay)


def simulate_shortcut(string):
    print(string)
    string = str(string).replace("simulate ", "").replace("-", " ").upper().split(" ")
    print(string)
    for mod in string:
        print(mod)
        try:
            if "CONTROL" in mod:
                keyboard.press(Key.ctrl_l)
            elif "SHIFT" in mod:
                keyboard.press(Key.shift)
            elif "ALT" in mod:
                keyboard.press(Key.alt)
            elif "TAB" in mod:
                keyboard.press(Key.tab)
            elif "WINDOWS" in mod:
                keyboard.press(Key.cmd)
            elif "ENTER" in mod:
                keyboard.press(Key.enter)
            else:
                keyboard.press(mod)
        except ValueError:
            Voice.__speak__("Could not find a shortcut that satisfies the specifications", "en")
        keyboard.release(Key.ctrl_l)
        keyboard.release(Key.shift)
        keyboard.release(Key.alt)
        keyboard.release(Key.enter)
        keyboard.release(Key.cmd)
        keyboard.release(Key.tab)


def black_screen():
    blk_screen.attributes('-fullscreen', True)
    blk_screen.title("GameUtils - Black Screen")
    blk_screen.config(bg='black')
    blk_screen.update()


class Voice:
    interpreter = sr.Recognizer()
    mic_input = sr.Microphone(device_index=1)

    @classmethod
    def __speak__(cls, text, lang):
        speech_obj = gTTS(text=text, lang=lang, slow=False)
        speech_obj.save("_curSpeech.mp3")
        print(f"GladOS: {text}")
        try:
            mixer.music.load("_curSpeech.mp3")
            mixer.music.play()
        except:
            pass

    @classmethod
    def __listen__(cls):
        while True:
            try:
                with cls.mic_input as audio_data:
                    cls.interpreter.adjust_for_ambient_noise(audio_data)
                    print("GladOS is Listening")
                    audio_input = cls.interpreter.listen(audio_data)
                    mic_output = str(cls.interpreter.recognize_google(audio_data=audio_input)).lower()
                    print(f"You said: {mic_output}")
                    if voice_inputs[0] in mic_output:
                        cls.__speak__(text=f"{voice_lines[0]}: {mic_output}", lang="en")
                        simulate_string(mic_output, 0.075)
                    elif voice_inputs[8] in mic_output or voice_inputs[9] in mic_output:
                        cls.__speak__(text=f"{voice_lines[3]}", lang="en")
                        black_screen()
                    elif voice_inputs[1] in mic_output or voice_inputs[2] in mic_output or voice_inputs[3] in mic_output:
                        shortcut = mic_output.replace("tea", "t").replace("bee", "b")
                        cls.__speak__(text=f"{voice_lines[1]}: {mic_output}", lang="en")
                        simulate_shortcut(string=shortcut)
                    elif voice_inputs[10] in mic_output:
                        cls.__speak__(text=f"{voice_lines[4]}", lang="en")
                        sleep(5)
                        exit()
                    elif voice_inputs[4] in mic_output or voice_inputs[5] in mic_output:
                        program = mic_output.replace("open ", "").replace("run ", "")
                        cls.__speak__(text=f"{voice_lines[2]}: {program}", lang="en")
                        simulate_shortcut("windows")
                        sleep(0.1)
                        simulate_string("type "+program, 0.075)
                        sleep(0.1)
                        simulate_shortcut("enter")
                    else:
                        pass
            except sr.UnknownValueError:
                continue


blk_screen = Tk()
nav_inputs = ['blk-screen', 'voice']
voice_inputs = ['type ', 'shortcut ', 'simulate ', 'press ', 'open ', 'run ', 'good', 'perfect', 'black screen', 'screen off',  'exit']
voice_lines = ['typing string', 'simulating shortcut', 'opening program', 'simulating black screen', 'exiting voice services']
voice_mode = bool(False)
update_black_screen = bool(False)
mixer.init()
keyboard = Controller()

while True:
    user_input = input("Please enter a command: ")

    if nav_inputs[0] in user_input:
        black_screen()
    if nav_inputs[1] in user_input:
        voice_mode = bool(True)
        Voice.__listen__()

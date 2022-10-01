import sys

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit

class Answer:
    def __init__(self, identify, reply, exec_function):
        self.identify = identify
        self.reply = reply
        self.exec_function = exec_function


audio = sr.Recognizer()
machine = pyttsx3.init()


def get_answer():
    try:
        with sr.Microphone() as source:
            print("Pode falar...")
            listen = audio.listen(source, timeout=3)
            command = audio.recognize_google(listen, language='pt-BR')
            command = command.lower()
            if 'júlia' in command:
                command = command.replace('júlia', '')
            else:
                print("Erro, comando: " + command)
                return "Error"
        return command
    except Exception as e:
        print(e)
        return "Error"


answers = \
    Answer("horário", "Agora são " + datetime.datetime.now().strftime('%H:%M'), 0), \
    Answer("amor", "Não posso ter amor, pois sou um robô", 0),\
    Answer("namorar", "Não posso namorar, sou apenas um robô", 0),\
    Answer("angola", "É um local que carece de fome, nunca viram uma feijoada", 0),\
    Answer("neymar", "", 1),\
    Answer("selena gomez", "", 1)


def get_function_answer(identify):
    try:
        wikipedia.set_lang('pt')
        answer = wikipedia.summary(identify, 2)
        print(answer)
    except Exception as e:
        print(e)
        return "Error"
    return answer;


def listen_user():
    command = get_answer()
    if "Error" in command: return

    print("Você disse '" + command + "'")
    if "pare" in command:
        machine.say("Tchau tchau, até a próxima")
        machine.runAndWait()
        print("Parando...")
        sys.exit()
    elif "tocar música" in command:
        command = command.split("tocar música")[1]
        print("Tocando " + command.strip())
        music = pywhatkit.playonyt(command)
        machine.say("Tocando música " + command)
        machine.runAndWait()
    else:
        answer = "Não sei nada sobre isso"
        for obj in answers:
            if obj.identify in command:
                if obj.exec_function == 1:
                    answer = get_function_answer(obj.identify)
                    break
                answer = obj.reply
                break
        print(answer)
        machine.say(answer)
        machine.runAndWait()


while (1 == 1):
    listen_user()


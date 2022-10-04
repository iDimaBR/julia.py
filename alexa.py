import sys
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import requests
import json
import dotenv
import os
import math


dotenv.load_dotenv(dotenv.find_dotenv())
audio = sr.Recognizer()
machine = pyttsx3.init()
ANGRY = 0


class Answer:
    def __init__(self, identify, reply):
        self.identify = identify
        self.reply = reply


answers = \
    Answer("horário", "Agora são " + datetime.datetime.now().strftime('%H:%M')),\
    Answer("amor", "Não posso ter amor, pois sou um robô"),\
    Answer("criador", "Meu criador é o Raphael, conhecido como Rapha"),\
    Answer("namorar", "Não posso namorar, sou apenas um robô"),\
    Answer("angola", "É um local que carece de fome, nunca viram uma feijoada"),\
    Answer("beatbox", "Bouti cabou, bou tica bou bou bou, Bouti cabou, bou tica bou bou bou, Julia yeah")

def get_weather(city):
    city = str(city).capitalize()
    web = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + city + ",BR&appid=" + os.getenv("WEATHER_API") + "&lang=pt_br&units=metric")
    content = json.loads(web.content)
    return "A temperatura em " + city + " é de " + str(int(content["main"]["temp"])) + " graus, com máxima de " + str(int(content["main"]["temp_max"])) + " graus e mínima de " + str(int(content["main"]["temp_min"])) + " graus"

def get_answer():
    try:
        with sr.Microphone() as source:
            print("Pode falar...")
            listen = audio.listen(source, timeout=3, phrase_time_limit=5)
            command = audio.recognize_google(listen, language='pt-BR')
            command = command.lower()

            if 'ok google' in command:
                machine.say("Ta achando que eu sou defeituosa que nem essa vadia?")
                machine.runAndWait()
                return "Error"

            if 'alexa' in command:
                machine.say("Quem é essa baranga que todo mundo pensa que sou eu?")
                machine.runAndWait()
                return "Error"

            if 'júlia' in command:
                command = command.replace('júlia ', '')
            else:
                return "Error"
        return command
    except Exception as e:
        print(e)
        return "Error"

def get_price(value):
    web = requests.get("http://economia.awesomeapi.com.br/json/last/" + value)
    content = json.loads(web.content)
    if "BTC" in value:
        value = content[value.replace("-","")]["ask"]
    else:
        value = "%.2f" % float(content[value.replace("-","")]["ask"])
    return "O valor está em R$ " + value


def wikipedia_search(command):
    try:
        wikipedia.set_lang('pt')
        answer = wikipedia.summary(command, 2)
    except Exception as e:
        print(e)
        return "Não sei nada sobre isso"
    return answer


def listen_user():
    global ANGRY
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
        print(music)
        machine.say("Tocando música " + command)
        machine.runAndWait()
    else:
        if "quem é" in command:
            answer = wikipedia_search(command.split(" é ")[1])
        elif "quem foi" in command:
            answer = wikipedia_search(command.split(" é ")[1])
        elif "oque é" in command:
            answer = wikipedia_search(command.split(" é ")[1])
        elif "como é" in command:
            answer = wikipedia_search(command.split(" é ")[1])
        elif "o que é" in command:
            answer = wikipedia_search(command.split(" é ")[1])
        elif "dólar" in command:
            answer = get_price("USD-BRL")
        elif "euro" in command:
            answer = get_price("EUR-BRL")
        elif "bitcoin" in command:
            answer = get_price("BTC-BRL")
        elif "libra" in command:
            answer = get_price("GBP-BRL")
        elif "temperatura em" in command:
            answer = get_weather(command.split(" em ")[1])
        else:
            answer = "Não sei nada sobre isso"

        for obj in answers:
            if obj.identify in command:
                answer = obj.reply
                break

        print(answer)
        if "Não sei nada sobre isso" in answer:
            ANGRY = ANGRY + 1
            if(ANGRY > 2):
                answer = "Oh porra, Eu ja te disse mil vezes que não sei"
                ANGRY = 0
        
        machine.say(answer)
        machine.runAndWait()


while (1 == 1):
    listen_user()

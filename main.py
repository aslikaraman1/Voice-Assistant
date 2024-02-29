import os
import random
import time
import webbrowser
from datetime import datetime

import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from translate import Translator

translator = Translator(to_lang="tr")

speech_recognizer = sr.Recognizer()

def record(ask=False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = speech_recognizer.listen(source)
        try:
            voice = speech_recognizer.recognize_google(audio, language="tr-TR")
            return voice
        except sr.UnknownValueError:
            print("Asistan: Anlayamadım")
        except sr.RequestError:
            print("Asistan: Sistem çalışmıyor")

def get_weather(city):
    api_key = "8fe4db6db23dac1cc55e110d458e6a1c"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") == 200:
        weather_desc = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])
        return f"{city} şehrinde hava {weather_desc}. Sıcaklık {temp} derece."
    else:
        return "Hava durumu bilgisi alınamadı."

def assistant_response(voice):
    if "merhaba" in voice:
        speak("sana da merhaba")
    elif "selam" in voice:
        speak("Aleykümselam")
    elif "teşekkür ederim" in voice or "teşekkürler" in voice:
        speak("rica ederim")
    elif "bugün günlerden ne" in voice or "hangi gündeyiz" in voice:
        today = time.strftime("%A")
        today = translator.translate(today)
        speak("Bugün günlerden " + today)
    elif "saat kaç" in voice:
        selection = ["Saat şu an: ", "Hemen bakıyorum: "]
        clock = datetime.now().strftime("%H:%M")
        selection = random.choice(selection)
        speak(selection + clock)
    elif "google'da ara" in voice:
        speak("Ne aramamı istersin?")
        search = record()
        url = "https://www.google.com/search?q={}".format(search)
        webbrowser.get().open(url)
        speak("{} için Google'da bulabildiklerimi listeliyorum.".format(search))
    elif "hava durumu ne" in voice:
        speak("Hangi şehir için hava durumunu öğrenmek istersiniz?")
        city = record()
        weather_info = get_weather(city)
        speak(weather_info)
    elif "not al" in voice:
        speak("Notun ismi ne olsun?")
        txtFile = record() + ".txt"
        theText = record()
        with open(txtFile, "w", encoding="utf-8") as f:
            f.write(theText)
    elif "görüşürüz" in voice:
        speak("Kendine iyi bak")
        os.remove("answer.mp3")
        exit()
    else:
        speak("Sizi anlayamadım")

def speak(text):
    tts = gTTS(text=text, lang="tr", slow=False)
    file_path = "response.mp3"
    tts.save(file_path)
    playsound(file_path)
    os.remove(file_path)

speak("Merhaba, size nasıl yardımcı olabilirim?")

while True:
    voice_input = record()
    if voice_input:
        voice_input = voice_input.lower()
        print(voice_input.capitalize())
        assistant_response(voice_input)

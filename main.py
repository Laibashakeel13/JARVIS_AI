import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from config import newsapi

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

pygame.mixer.init()

pygame.mixer.music.load("temp.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

os.remove("temp.mp3")


def aiprocess(c):
    client = OpenAI(api_key = "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")
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        
        {
            "role": "user","content": c  }
    ]
)
    return completion.choices[0].message.content

def process_command(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("http://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("http://facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("http://youtube.com")
    elif "open netflix" in command:
        speak("Opening Netflix")
        webbrowser.open("http://netflix.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("http://linkedin.com")
    elif command.startswith("play"):
        song = command.split("play", 1)[1].strip()  
        if song in musiclibrary.music:
            speak(f"Playing {song}")
            link = musiclibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have {song} in my library.")
    elif "news" in command.lower():  
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        r = requests.get(url)
        
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            
            if articles:
                for a in articles[:5]:  
                    speak(a['title'])
            else:
                speak("Sorry, I couldn't find any news articles.")
        else:
            speak("Sorry, I couldn't retrieve the news at the moment.")
    else:
        speak("I didn't understand the command. Could you please repeat it?")
        print(f"Unrecognized command: {command}")  
        output= OpenAI(command)
        speak(output)

if __name__ == "__main__":
    speak("Hello Laiba, how may I help you today?")  

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  
                print("Listening for 'Jarvis'...")

                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            
            try:
                wake_word = recognizer.recognize_google(audio)
                print(f"Wake word recognized: {wake_word}")  
                if wake_word.lower() == "jarvis":
                    speak("Yes, I am here.")
                    
                    with sr.Microphone() as source:
                        print("Listening for your command...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)

                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")  
                    process_command(command)

            except sr.UnknownValueError:
                print("Wake word not detected. Please say 'Jarvis'.")
            except sr.RequestError as e:
                speak("Sorry, I couldn't connect to the speech recognition service.")
                print(f"Error with Google API: {e}")

        except sr.WaitTimeoutError:
            print("Listening timed out. Please try speaking again.")
        except Exception as e:
            print(f"Error: {e}")

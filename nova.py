import os
import subprocess
import webbrowser
import time
import re
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# === CONFIGURATION ===

OPENROUTER_API_KEY = "sk-or-your-api-key-here"  # Replace with your OpenRouter API key

# Update these paths:
CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"
CHROME_PROFILE_PATH = r"C:\Users\Aman\AppData\Local\Google\Chrome\User Data\Profile 10"

WAKE_WORDS = ["nova", "hey nova", "ok nova"]

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print(f"NOVA says: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command(timeout=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=timeout)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the speech service.")
        return ""

def call_openrouter_api(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        speak("I'm having trouble reaching the server.")
        return None

def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    speak(f"Opening {url.replace('https://', '').replace('http://', '')}")
    webbrowser.open(url)

def open_app(app_name):
    app_name = app_name.lower().strip()

    common_apps = {
        "camera": "microsoft.windows.camera:",
        "calculator": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "task manager": "taskmgr.exe",
        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        "spotify": r"C:\Users\Aman\AppData\Roaming\Spotify\Spotify.exe",
    }

    if app_name in common_apps:
        target = common_apps[app_name]
        if target.endswith(".exe"):
            try:
                subprocess.Popen(target)
                speak(f"Opening {app_name}")
                return True
            except Exception as e:
                speak(f"Sorry, I couldn't open {app_name}")
                print(f"Error opening {app_name}: {e}")
                return False
        else:
            try:
                subprocess.Popen(["start", target], shell=True)
                speak(f"Opening {app_name}")
                return True
            except Exception as e:
                speak(f"Sorry, I couldn't open {app_name}")
                print(f"Error opening {app_name}: {e}")
                return False

    try:
        subprocess.Popen(f'start "" "{app_name}"', shell=True)
        speak(f"Opening {app_name}")
        return True
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}")
        print(f"Error opening {app_name}: {e}")
        return False

def close_app(app_name):
    app_name = app_name.lower().strip()
    process_names = {
        "chrome": "chrome.exe",
        "brave": "brave.exe",
        "notepad": "notepad.exe",
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        "calculator": "Calculator.exe",
        "camera": "WindowsCamera.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "task manager": "Taskmgr.exe",
    }

    proc = process_names.get(app_name, app_name + ".exe")
    try:
        subprocess.run(f"taskkill /f /im {proc}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        speak(f"Closing {app_name}")
        return True
    except Exception as e:
        speak(f"Sorry, I couldn't close {app_name}")
        print(f"Error closing {app_name}: {e}")
        return False

def play_youtube_song(song_name):
    speak(f"Playing {song_name} on YouTube")
    options = Options()
    options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(CHROMEDRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        search_query = song_name.replace("play", "").strip()
        driver.get(f"https://www.youtube.com/results?search_query={search_query}")
        time.sleep(4)
        videos = driver.find_elements("id", "video-title")
        if videos:
            videos[0].click()
            return True
        else:
            speak("Sorry, I couldn't find the video.")
            return False
    except Exception as e:
        print(f"YouTube Error: {e}")
        speak("Sorry, I couldn't play the video.")
        return False

def shutdown_pc():
    speak("Shutting down the computer immediately.")
    subprocess.run("shutdown /s /f /t 0", shell=True)

def process_command(command):
    command = command.lower()
    print(f"Processing command: '{command}'")

    for wake in WAKE_WORDS:
        if command.startswith(wake):
            command = command[len(wake):].strip()
            break

    if command.startswith("open "):
        target = command[5:].strip()
        if target.endswith(".com") or target.startswith("www.") or "http" in target:
            open_website(target)
        elif "youtube" in target and "play" in target:
            song = target.replace("youtube", "").replace("play", "").strip()
            play_youtube_song(song)
        else:
            open_app(target)
        return True

    if command.startswith("close "):
        target = command[6:].strip()
        close_app(target)
        return True

    if command.startswith("play "):
        song = command[5:].strip()
        play_youtube_song(song)
        return True

    if "shutdown" in command or "shut down" in command:
        shutdown_pc()
        return True

    response = call_openrouter_api(command)
    if response:
        speak(response)
        return True
    else:
        speak("Sorry, I didn't understand that.")
        return False

def main():
    speak("Hello sir, how may I help you?")
    while True:
        command = listen_command(timeout=7)
        if not command:
            continue

        if any(wake in command for wake in WAKE_WORDS):
            for wake in WAKE_WORDS:
                if wake in command:
                    command = command.replace(wake, "").strip()
                    break
            if command:
                process_command(command)

if __name__ == "__main__":
    main()

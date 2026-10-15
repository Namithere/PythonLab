import os
import sys
import time
import pyttsx3
import pyautogui
import speech_recognition as sr



def init_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # Speed
    engine.setProperty("volume", 0.6)  # Volume
    return engine


engine = init_engine()


def speak(text):
    print(f"\n[Assistant]: {text}")
    engine.say(text)
    engine.runAndWait()


#Listener Class
recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:
        print("\n Listening for a command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print(" Processing speech...")
            command = recognizer.recognize_google(audio)
            print(f" You said: '{command}'")
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print(" Couldn't understand audio.")
            return ""
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return (""
                    "")


#Command Substitutes
def process_command(command):
    #App
    if "open notepad" in command:
        speak("Opening Notepad...")
        if sys.platform == "win32":
            os.system("start notepad")
        else:
            print("Not usable")
    elif "open word" in command:
        speak("Opening Microsoft Word...")
        if sys.platform == "win32":
            os.system("start winword")
        else:
            print("Not usable")
        time.sleep(2)  # Allow time for app to load

    # Typing Substitues
    elif command.startswith("type "):

        text_to_type = command.replace("type ", "", 1)
        speak("Typing text...")

        pyautogui.write(text_to_type + " ", interval=0.03)

    elif command == "type" or command == "start typing":
        speak("What would you like me to type?")
        dictation = listen()
        if dictation:
            speak("Typing...")
            pyautogui.write(dictation + " ", interval=0.03)

    # Keyboerd Substitutes
    elif "press enter" in command or "new line" in command:
        pyautogui.press("enter")

    elif "backspace" in command or "delete text" in command:
        pyautogui.press("backspace")

    elif "save file" in command or "save document" in command:
        speak("Saving document...")
        pyautogui.hotkey("ctrl", "s")  # Use ('command', 's') on macOS

    elif "select all" in command:
        pyautogui.hotkey("ctrl", "a")

    # Stop This Madness
    elif any(word in command for word in ["exit", "stop", "quit", "goodbye"]):
        speak("Goodbye! Shutting down assistant.")
        return False

    return True


#Main Code
if __name__ == "__main__":
    speak("Voice assistant online. How can I help you today?")
    running = True

    while running:
        user_input = listen()
        if user_input:
            running = process_command(user_input)
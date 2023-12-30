import os
import time
import pyautogui
import speech_recognition as sr
import pyttsx3
import psutil

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Define the takecommand function to capture voice input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}") 
            return ""

# Define the speak function to output voice response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define the JarvisAssistant class
class JarvisAssistant:
    def __init__(self):
        pass

    def run(self):
        while True:
            self.query = takecommand().lower()

            # Open Spotify and play the current song
            if 'open spotify' in self.query or 'play the current song' in self.query:
                speak("Opening Spotify and playing the current song.")
                os.startfile("Spotify.exe")  # Replace with your Spotify path
                #time.sleep(10)  # Wait for Spotify to open
                pyautogui.press('space')  # Play the song
                speak("Yes, I am playing the current song.")

            # Like the current song
            elif 'like the song' in self.query:
                speak("Liking the current song.")
                pyautogui.click(x=1100, y=650)  # Assuming the like button coordinates
                pyautogui.hotkey('alt', 'shift', 'b', interval=0.25)
                speak("Song liked successfully.")
            
            # Pause the current song
            elif 'pause the song' in self.query:
                speak("Pausing the current song.")
                os.startfile("Spotify.exe")
                pyautogui.press('space')  # Pause the song in Spotify
                speak("Song paused successfully.")
            
            # Handle unrecognized commands
            else:
                speak("Sorry, I did not understand that command. Please try again.")

# Create an instance of the JarvisAssistant class and run the assistant
if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
  

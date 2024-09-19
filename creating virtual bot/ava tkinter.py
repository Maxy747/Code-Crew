import tkinter as tk
import threading
import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import wikipedia.exceptions
import pyautogui
import sys

# Initialize the voice assistant engine
listener = aa.Recognizer()
ava = pyttsx3.init()

# Set feminine voice and speaking rate
voices = ava.getProperty('voices')
ava.setProperty('voice', voices[1].id)
ava.setProperty('rate', 150)

# Global variable to control the assistant
running = False

# Function to make Ava speak
def talk(text):
    ava.say(text)
    ava.runAndWait()

# Function to capture voice input
def input_instruction():
    global instruction
    instruction = ""
    try:
        with aa.Microphone() as origin:
            print("Listening...")
            listener.adjust_for_ambient_noise(origin)
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "ava" in instruction:
                instruction = instruction.replace('ava', '').strip()
                print(f"Command after removing 'ava': {instruction}")
            print(f"Recognized Instruction: {instruction}")
    except aa.UnknownValueError:
        print("Sorry, I did not understand that.")
        talk("Sorry, I did not understand that.")
    except aa.RequestError:
        print("Sorry, the service is down.")
        talk("Sorry, the service is down.")
    
    return instruction

# Function to handle cursor movements
def control_cursor(instruction):
    if "move up" in instruction:
        pyautogui.moveRel(0, -150)  # Move up
        talk("Moving up")
    elif "move down" in instruction:
        pyautogui.moveRel(0, 150)  # Move down
        talk("Moving down")
    elif "move left" in instruction:
        pyautogui.moveRel(-150, 0)  # Move left
        talk("Moving left")
    elif "move right" in instruction:
        pyautogui.moveRel(150, 0)  # Move right
        talk("Moving right")
    elif "click" in instruction:
        pyautogui.click()  # Perform a click
        talk("Clicking")
    elif "scroll up" in instruction:
        pyautogui.scroll(100)  # Scroll up
        talk("Scrolling up")
    elif "scroll down" in instruction:
        pyautogui.scroll(-100)  # Scroll down
        talk("Scrolling down")
    else:
        talk("Command not recognized.")

# Function to run the assistant in a thread
def play_Ava():
    global running
    while running:
        instruction = input_instruction()

        if "stop" in instruction or "exit" in instruction:
            talk("Stopping the assistant.")
            print("Exiting the program.")
            running = False  # Stop the assistant
            break

        if "play" in instruction:
            song = instruction.replace('play', "").strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f'Current time is {time}')

        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk(f"Today's date is {date}")

        elif 'how are you' in instruction:
            talk('I am fine, how about you?')

        elif 'what is your name' in instruction:
            talk('I am Ava, what can I do for you?')

        elif 'who is' in instruction or 'what is' in instruction:
            try:
                human = instruction.replace('who is', "").replace('what is', "").strip()
                print(f"Searching Wikipedia for: {human}")
                info = wikipedia.summary(human, sentences=2)
                print(f"Wikipedia Summary: {info}")
                talk(info)
            except wikipedia.exceptions.PageError:
                talk(f"Sorry, I couldn't find information on {human}.")
            except wikipedia.exceptions.DisambiguationError as e:
                talk(f"Your query is ambiguous. Here are some options: {', '.join(e.options)}")
            except Exception as e:
                print(f"An error occurred: {e}")
                talk("Sorry, there was an issue processing your request.")
        else:
            control_cursor(instruction)

# Function to start the assistant thread
def start_assistant():
    global running
    running = True
    talk("Hello, Ava at your service")  # Greet the user
    assistant_thread = threading.Thread(target=play_Ava)
    assistant_thread.start()

# Function to stop the assistant
def stop_assistant():
    global running
    running = False
    talk("Goodbye boss!")

# Set up the colored Tkinter interface
def create_interface():
    window = tk.Tk()
    window.title("Ava - Voice Assistant")
    window.geometry("400x300")
    window.configure(bg="#f0f0f0")  # Background color from Figma design

    title_label = tk.Label(window, text="Ava - Voice Assistant", bg="#333333", fg="#ffffff", font=("Arial", 16), pady=10)
    title_label.pack(fill=tk.X)

    info_label = tk.Label(window, text="Give commands to Ava!", bg="#f0f0f0", font=("Arial", 12))
    info_label.pack(pady=10)

    # Buttons with customized colors
    start_button = tk.Button(window, text="Start", command=start_assistant, bg="#4CAF50", fg="#ffffff", padx=20, pady=10)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop", command=stop_assistant, bg="#f44336", fg="#ffffff", padx=20, pady=10)
    stop_button.pack(pady=10)

    window.mainloop()

# Create the interface
if __name__ == "__main__":
    create_interface()

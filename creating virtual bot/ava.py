import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import wikipedia.exceptions
import pyautogui
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Initialize recognizer and text-to-speech engine
listener = aa.Recognizer()
ava = pyttsx3.init()

# Set feminine voice
voices = ava.getProperty('voices')
ava.setProperty('voice', voices[1].id)  # Select the second voice, typically feminine
ava.setProperty('rate', 150)  # Adjust speed if needed

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
            print("Tryin to hear...")
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

# Function to control cursor based on voice commands
def control_cursor(instruction):
    if "move up" in instruction:
        pyautogui.moveRel(0, -150)  # Move up by 50 pixels
        talk("Moving up")
    elif "move down" in instruction:
        pyautogui.moveRel(0, 150)  # Move down by 50 pixels
        talk("Moving down")
    elif "move left" in instruction:
        pyautogui.moveRel(-150, 0)  # Move left by 50 pixels
        talk("Moving left")
    elif "move right" in instruction:
        pyautogui.moveRel(150, 0)  # Move right by 50 pixels
        talk("Moving right")
    elif "click" in instruction:
        pyautogui.click()  # Perform a mouse click
        talk("Clicking")
    elif "scroll up" in instruction:
        pyautogui.scroll(100)  # Scroll up
        talk("Scrolling up")
    elif "scroll down" in instruction:
        pyautogui.scroll(-100)  # Scroll down
        talk("Scrolling down")
    else:
        talk(' command not recognized.')

# Main function to handle Ava's responses
def play_Ava():
    while True:
        instruction = input_instruction()
        
        if "stop" in instruction or "exit" in instruction:
            talk("Stopping the assistant.")
            print("Exiting the program.")
            break  # Exit the loop and stop the program
        
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
                # Handle both 'who is' and 'what is'
                human = instruction.replace('who is', "").replace('what is', "").strip()
                print(f"Searching Wikipedia for: {human}")  # Debugging output
                info = wikipedia.summary(human, sentences=2)
                print(f"Wikipedia Summary: {info}")  # Debugging output
                talk(info)
            except wikipedia.exceptions.PageError:
                talk(f"Sorry, I couldn't find information on {human}.")
            except wikipedia.exceptions.DisambiguationError as e:
                talk(f"Your query is ambiguous. Here are some options: {', '.join(e.options)}")
            except Exception as e:
                print(f"An error occurred: {e}")
                talk("Sorry, there was an issue processing your request.")

        else:
            control_cursor(instruction)  # Handle cursor-related commands

# Run the assistant
play_Ava()

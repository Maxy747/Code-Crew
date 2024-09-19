import sys
sys.stdout.reconfigure(encoding='utf-8')
import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# Initialize recognizer and text-to-speech engine
listener = aa.Recognizer()
machine = pyttsx3.init()

# Function to make the assistant speak
def talk(text):
    try:
        # Attempt to say the text normally
        machine.say(text)
        machine.runAndWait()
    except UnicodeEncodeError:
        # Handle non-ASCII characters by removing them
        cleaned_text = text.encode("ascii", "ignore").decode("ascii")
        machine.say(cleaned_text)
        machine.runAndWait()

# Function to capture voice input
def input_instruction():
    global instruction
    instruction = ""
    try:
        with aa.Microphone() as origin:
            print("listening...")
            listener.adjust_for_ambient_noise(origin)  # Adjusts for background noise
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "adam" in instruction:
                instruction = instruction.replace('adam', '')  # Remove 'adam' from command
                print(f"Command after removing 'adam': {instruction}")
            print(f"Recognized Instruction: {instruction}")

    except aa.UnknownValueError:
        print("Sorry, I did not understand that.")
        talk("Sorry, I did not understand that.")
    except aa.RequestError:
        print("Sorry, the service is down.")
        talk("Sorry, the service is down.")
    
    return instruction

# Main function to handle the assistant's responses
def play_Adam():
    instruction = input_instruction()  # Get instruction
    if "play" in instruction:
        song = instruction.replace('play', "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)  # Plays the song on YouTube
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date}")
    elif 'how are you' in instruction:
        talk('I am fine, how about you?')
    elif 'what is your name' in instruction:
        talk('I am Adam, what can I do for you?')
    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        try:
            # Try to fetch a summary from Wikipedia
            info = wikipedia.summary(human, sentences=2)
            print(info)  # Print the info to the console
            talk(info)  # Speak the Wikipedia info
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"Multiple entries found for {human}. Please be more specific.")
            print(f"Disambiguation Error: {e.options}")  # Log possible options
        except wikipedia.exceptions.PageError:
            # If a direct page lookup fails, try a search as a fallback
            search_results = wikipedia.search(human)
            if search_results:
                first_result = search_results[0]
                try:
                    info = wikipedia.summary(first_result, sentences=2)
                    print(f"First search result: {first_result}")
                    print(info)  # Print the info to the console
                    talk(info)  # Speak the Wikipedia info
                except wikipedia.exceptions.PageError:
                    talk(f"Could not retrieve information for {first_result}.")
            else:
                talk(f"Sorry, I could not find any information on {human}.")
                print(f"PageError: No result found for {human}.")
        except Exception as e:
            talk("Sorry, something went wrong.")
            print(f"An error occurred: {e}")
    else:
        talk('Please repeat your command.')

# Run the assistant
play_Adam()

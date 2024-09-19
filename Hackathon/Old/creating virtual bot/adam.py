import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = aa.Recognizer()
machine = pyttsx3.init()


def talk(text):
    machine.say(text)
    machine.runAndWait()  


def input_instruction():
    global instruction
    instruction = ""
    try:
        with aa.Microphone() as origin:
            print("listening...")
            listener.adjust_for_ambient_noise(origin)  
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "adam" in instruction:
                instruction = instruction.replace('adam', '')  
                print(f"Command after removing 'adam': {instruction}")
            print(f"Recognized Instruction: {instruction}")

    except aa.UnknownValueError:
        print("Sorry, I did not understand that.")
        talk("Sorry, I did not understand that.")
    except aa.RequestError:
        print("Sorry, the service is down.")
        talk("Sorry, the service is down.")
    
    return instruction


def play_Adam():
    instruction = input_instruction()  
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
        talk('I am Adam, what can I do for you?')
    elif 'who is' in instruction:
        try:
            human = instruction.replace('who is', "").strip()
            info = wikipedia.summary(human, sentences=1)  # Get the summary from Wikipedia
            print(info)
            talk(info)  # Speak the retrieved info
        except wikipedia.exceptions.PageError:
            print(f"Sorry, I couldn't find any information on {human}.")
            talk(f"Sorry, I couldn't find any information on {human}.")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Multiple results found for {human}. Be more specific.")
            talk(f"Multiple results found for {human}. Be more specific.")
        except Exception as e:
            print(f"An error occurred: {e}")
            talk("Sorry, something went wrong.")

    else:
        talk('Please repeat your command.')

# Run the assistant
play_Adam()

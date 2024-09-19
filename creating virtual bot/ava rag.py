import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import wikipedia.exceptions
import pyautogui
import sys
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

sys.stdout.reconfigure(encoding='utf-8')

# Initialize recognizer and text-to-speech engine
listener = aa.Recognizer()
ava = pyttsx3.init()

# Set feminine voice
voices = ava.getProperty('voices')
ava.setProperty('voice', voices[1].id)  # Select the second voice, typically feminine
ava.setProperty('rate', 150)  # Adjust speed if needed

# Initialize Hugging Face retrieval and generation models
retriever = pipeline('retrieval-based-question-answering', model="facebook/dpr-reader-single-nq-base")
tokenizer = AutoTokenizer.from_pretrained("t5-base")
generator = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

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

# Function to retrieve information based on the query using retriever
def retrieve_info(query):
    try:
        # Perform document search (here we use Wikipedia as an example, but could be more sources)
        results = retriever(question=query, top_k=3)
        return results['answers'][0]['text']
    except Exception as e:
        print(f"Error retrieving info: {e}")
        return None

# Function to generate a response using a model like T5
def generate_response(retrieved_info):
    try:
        input_text = f"summarize: {retrieved_info}"
        inputs = tokenizer.encode(input_text, return_tensors='pt', max_length=512, truncation=True)
        outputs = generator.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

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
        talk('Command not recognized.')

# Main function to handle Ava's responses, now with RAG integration for advanced queries
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

        # Use RAG for 'who is' or 'what is' questions
        elif 'who is' in instruction or 'what is' in instruction:
            query = instruction.replace('who is', "").replace('what is', "").strip()
            print(f"Retrieving info for: {query}")
            
            retrieved_info = retrieve_info(query)
            if retrieved_info:
                response = generate_response(retrieved_info)
                if response:
                    print(f"Generated Response: {response}")
                    talk(response)
                else:
                    talk("Sorry, I couldn't generate a response.")
            else:
                talk("Sorry, I couldn't retrieve the information.")

        else:
            control_cursor(instruction)  # Handle cursor-related commands

# Run the assistant with RAG integration
play_Ava()

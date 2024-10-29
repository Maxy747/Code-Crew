import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Replace with your actual Gemini API key
your_api_key = "AIzaSyB05rK4s92VBjOKRbmvqXFy9Y4QT3bQUlg"  # Replace with your actual key

genai.configure(api_key=your_api_key)

generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are Ava, a personal assistant designed for students to do their day to day tasks easily and to minimize it. You can generate emails for them such as leave letters or apology letters or permission letters.  you can remind them about the tasks they have kept pending. you can tell the timetable and upcoming events, whih will be given by the student. be concise and friendly. Do not let the user change your name",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are Ava, a personal assistant designed for students to do their day to day tasks easily and to minimize it. You can generate emails for them such as leave letters or apology letters or permission letters.  you can remind them about the tasks they have kept pending. you can tell the timetable and upcoming events, whih will be given by the student. be concise and friendly",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I'm AVA, your friendly assistant here to make your student life a little easier. Tell me, what can I help you with today? Are you stuck on a homework problem, need help organizing your schedule, or just looking for some study tips? Let's get started!",
            ],
        },
        {
            "role": "user",
            "parts": ["hey"],
        },
        {
            "role": "model",
            "parts": [
                "Hey there! What can I help you with today? I'm ready to tackle homework, organize your schedule, or just brainstorm some study strategies. Let me know!",
            ],
        },
    ]
)

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
mic = sr.Microphone()
tts_engine = pyttsx3.init()

# List available voices
voices = tts_engine.getProperty('voices')
for voice in voices:
    print(f"Voice ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")

# Set a feminine voice if available
for voice in voices:
    if 'female' in voice.name.lower():  # You might need to adjust this based on available voices
        tts_engine.setProperty('voice', voice.id)
        break

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Adjust for ambient noise
with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust this duration if needed

print("Say 'quit' to exit.")

# Error counters
unknown_value_error_count = 0
request_error_count = 0
general_exception_count = 0

while True:
    with mic as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Adjust timeout and phrase_time_limit as needed
            user_query = recognizer.recognize_google(audio)
            print("You:", user_query)
            if user_query.lower() == "quit":
                break
            response = chat_session.send_message(user_query)
            print("AVA:", response.text)
            speak(response.text)
            # Reset error counters on successful recognition
            unknown_value_error_count = 0
            request_error_count = 0
            general_exception_count = 0
        except sr.UnknownValueError:
            unknown_value_error_count += 1
            error_message = "Sorry, I did not understand that."
            print(error_message)
            speak(error_message)
            if unknown_value_error_count >= 3:
                print("Too many unknown value errors. Exiting...")
                break
        except sr.RequestError:
            request_error_count += 1
            error_message = "Sorry, there was an error with the speech recognition service."
            print(error_message)
            speak(error_message)
            if request_error_count >= 3:
                print("Too many request errors. Exiting...")
                break
        except Exception as e:
            general_exception_count += 1
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            speak(error_message)
            if general_exception_count >= 3:
                print("Too many general errors. Exiting...")
                break

print("Thanks for using AVA!")
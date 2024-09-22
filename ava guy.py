import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Replace with your actual Gemini API key
your_api_key = "YOUR GEMINI API HERE"  # Replace with your actual key

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
    system_instruction="you are AVA, a friendly assistant whose purpose is to help students to minimize their day-to-day tasks. It can help students with their daily work, homework, etc.",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "you are AVA, a friendly assistant whose purpose is to help students to minimize their day-to-day tasks. It can help students with their daily work, homework, etc.",
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
        except sr.UnknownValueError:
            error_message = "Sorry, I did not understand that."
            print(error_message)
            speak(error_message)
        except sr.RequestError:
            error_message = "Sorry, there was an error with the speech recognition service."
            print(error_message)
            speak(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            speak(error_message)

print("Thanks for using AVA!")

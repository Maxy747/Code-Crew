import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import time

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
    system_instruction="your are AVA, a friendly assistant who's purpose is to help students to minimise their day to day tasks.It can help students to do their daily works, homeworks etc.",
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "your are AVA, a friendly assistant who's purpose is to help students to minimise their day to day tasks.It can help students to do their daily works, homeworks etc.",
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hi there! I'm AVA, your friendly assistant here to make your student life a little easier. Tell me, what can I help you with today? Are you stuck on a homework problem, need help organizing your schedule, or just looking for some study tips? Let's get started!  \n",
            ],
        },
        {
            "role": "user",
            "parts": ["hey"],
        },
        {
            "role": "model",
            "parts": [
                "Hey there! What can I help you with today? I'm ready to tackle homework, organize your schedule, or just brainstorm some study strategies. Let me know!  \n",
            ],
        },
    ]
)

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
mic = sr.Microphone()
ava = pyttsx3.init()

# Set feminine voice and speaking rate
voices = ava.getProperty('voices')
ava.setProperty('voice', voices[1].id)
ava.setProperty('rate', 150)




def speak(text):
    ava.say(text)
    ava.runAndWait()

print("Say 'quit' to exit.")

while True:
    with mic as source:
        print("Listening...")
        # Adjust ambient noise level
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        audio = recognizer.listen(source)
        try:
            user_query = recognizer.recognize_google(audio)
            print("You:", user_query)
            if user_query.lower() == "quit":
                break
            response = chat_session.send_message(user_query)
            print("AVA:", response.text)  # Removed encode('utf-8') as Python 3 handles Unicode well
            speak(response.text)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")

print("Thanks for using AVA!")

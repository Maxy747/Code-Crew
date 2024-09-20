import google.generativeai as genai
import pyttsx3
import pywhatkit as kit
import speech_recognition as sr

# Configure the API key directly (not recommended for production, but useful for testing)
genai.configure(api_key="AIzaSyDfdcqenqguK8NV6gYa-Tn_gEFW0uy2nCg")

# Create the model
generation_config = {
    "temperature": 1.3,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are Ava, a personal assistant designed for students to do their day-to-day tasks easily. Be concise and friendly.",
)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice and rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index to select a different voice
engine.setProperty('rate', 150)  # Set speaking rate

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Start the chat session with a pre-existing conversation history
chat_session = model.start_chat(
    history=[
        {"role": "user", "parts": ["hi"]},
        {"role": "model", "parts": ["Hi there! How can I help you today?"]},
    ]
)

# Function to play a YouTube video
def play_youtube_video(video_title):
    try:
        kit.playonyt(video_title)  # Use pywhatkit to play the video
        return f"Playing '{video_title}' on YouTube."
    except Exception as e:
        return f"Sorry, I couldn't play the video. {str(e)}"

# Function to listen for user input via microphone
def listen_for_input():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
        # Set timeout to 10 seconds for testing
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return ""

# Function to get user input and interact with the assistant
def interact_with_assistant():
    print("You can start speaking your messages. Type 'exit' or 'quit' to stop.")
    while True:
        # Listen for user input
        user_input = listen_for_input()
        if user_input.lower() in ["exit", "quit"]:  # Exit condition
            print("Goodbye!")
            break
        # Check if the user wants to play a YouTube video
        if "play" in user_input.lower() and "youtube" in user_input.lower():
            video_title = user_input.lower().replace("play", "").replace("youtube", "").strip()
            response_text = play_youtube_video(video_title)
        else:
            # Send user input to the assistant
            response = chat_session.send_message(user_input)
            response_text = response.text

        # Print the response from the assistant
        print(f"Ava: {response_text}")
        # Read the response aloud
        engine.say(response_text)
        engine.runAndWait()

# Call the function to start interaction
interact_with_assistant()

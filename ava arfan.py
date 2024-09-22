import os
import datetime
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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

class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def _init_(self):
        self.creds = self.get_credentials()
        self.service = build("calendar", "v3", credentials=self.creds)

    def get_credentials(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def list_events(self, time_min=None, time_max=None, max_results=10):
        if time_min is None:
            time_min = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=time_min,
                                                   timeMax=time_max, maxResults=max_results,
                                                   singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, summary, description, location, start_time, end_time):
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }
        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        return f'Event created: {created_event.get("htmlLink")}'

    def update_event(self, event_id, summary, description, location, start_time, end_time):
        updated_event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
        }
        self.service.events().update(calendarId='primary', eventId=event_id, body=updated_event).execute()
        return "Event updated successfully."

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        return "Event deleted successfully."

    def retrieve_events_in_month(self, year, month):
        start_date = datetime.datetime(year, month, 1)
        end_date = datetime.datetime(year + (month // 12), (month % 12) + 1, 1)
        time_min = start_date.isoformat() + 'Z'
        time_max = end_date.isoformat() + 'Z'
        return self.list_events(time_min=time_min, time_max=time_max)

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

def main():
    # Initialize Google Calendar
    calendar = GoogleCalendar()
    print("Say 'quit' to exit.")
    
    while True:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1) 
            audio = recognizer.listen(source)
            try:
                user_query = recognizer.recognize_google(audio)
                print("You:", user_query)

                if user_query.lower() == "quit":
                    break

                # Process calendar commands
                if "create event" in user_query:
                    summary = input("Enter event summary: ")
                    description = input("Enter event description: ")
                    location = input("Enter event location: ")
                    start_time = input("Enter start time (YYYY-MM-DDTHH:MM:SS): ")
                    end_time = input("Enter end time (YYYY-MM-DDTHH:MM:SS): ")
                    response = calendar.create_event(summary, description, location, start_time, end_time)
                    print("AVA:", response)
                    speak(response)

                elif "update event" in user_query:
                    event_id = input("Enter event ID to update: ")
                    summary = input("Enter new event summary: ")
                    description = input("Enter new event description: ")
                    location = input("Enter new event location: ")
                    start_time = input("Enter new start time (YYYY-MM-DDTHH:MM:SS): ")
                    end_time = input("Enter new end time (YYYY-MM-DDTHH:MM:SS): ")
                    response = calendar.update_event(event_id, summary, description, location, start_time, end_time)
                    print("AVA:", response)
                    speak(response)

                elif "delete event" in user_query:
                    event_id = input("Enter event ID to delete: ")
                    response = calendar.delete_event(event_id)
                    print("AVA:", response)
                    speak(response)

                elif "events in" in user_query:
                    year, month = map(int, input("Enter year and month (YYYY MM): ").split())
                    events = calendar.retrieve_events_in_month(year, month)
                    if not events:
                        response = "No events found."
                    else:
                        response = "Here are your events: " + ", ".join(event['summary'] for event in events)
                    print("AVA:", response)
                    speak(response)

                else:
                    response = "Sorry, I did not understand that command."
                    print("AVA:", response)
                    speak(response)

            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")

    print("Thanks for using AVA!")

if _name_ == "_main_":
    main()

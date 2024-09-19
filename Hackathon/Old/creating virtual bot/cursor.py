import pyautogui
import speech_recognition as sr
import sys

# Initialize recognizer
listener = sr.Recognizer()

# Function to capture voice input
def input_instruction():
    global instruction
    instruction = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            print(f"Recognized Instruction: {instruction}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Sorry, the service is down.")
    
    return instruction

# Function to move the cursor based on voice commands
def control_cursor(instruction):
    if "move up" in instruction:
        pyautogui.moveRel(0, -50)  # Move up by 50 pixels
    elif "move down" in instruction:
        pyautogui.moveRel(0, 50)  # Move down by 50 pixels
    elif "move left" in instruction:
        pyautogui.moveRel(-500, 0)  # Move left by 50 pixels
    elif "move right" in instruction:
        pyautogui.moveRel(500, 0)  # Move right by 50 pixels
    elif "click" in instruction:
        pyautogui.click()  # Perform a mouse click
    elif "scroll up" in instruction:
        pyautogui.scroll(100)  # Scroll up
    elif "scroll down" in instruction:
        pyautogui.scroll(-100)  # Scroll down
    else:
        print("Command not recognized.")

# Main function to run the assistant
def main():
    while True:
        instruction = input_instruction()
        control_cursor(instruction)

# Run the assistant
main()

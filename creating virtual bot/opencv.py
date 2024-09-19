import cv2
import numpy as np
import pytesseract
import pyttsx3

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Adjust speed if needed

# Configure the path to the Tesseract executable (adjust if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows path, adjust if necessary

# Function to make the bot speak
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to detect hand gestures and read text
def detect_gesture_and_read_text(frame):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color range for skin detection
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a binary mask where skin color is detected
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Apply mask to get the segmented skin region
    skin = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Convert the mask to grayscale for contour detection
    gray_mask = cv2.cvtColor(skin, cv2.COLOR_BGR2GRAY)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(gray_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) < 5000:
            continue
        
        # Draw the contour
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        
        # Get the convex hull of the contour
        hull = cv2.convexHull(contour)
        
        # Draw the convex hull
        cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)
        
        # Find the convexity defects
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)
        
        # Count the number of defects to identify gestures
        if defects is not None:
            count_defects = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                if d > 10000:  # Minimum defect depth
                    count_defects += 1
                    cv2.circle(frame, (f[0], f[1]), 5, (0, 0, 255), -1)
            
            # Determine the gesture based on the number of defects
            if count_defects == 1:
                gesture = "One Finger"
            elif count_defects == 2:
                gesture = "Two Fingers"
            elif count_defects == 3:
                gesture = "Three Fingers"
            else:
                gesture = "Unknown Gesture"
            
            # Display the detected gesture
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            # Extract text from the detected hand region
            x, y, w, h = cv2.boundingRect(contour)
            hand_region = gray_mask[y:y+h, x:x+w]
            text = pytesseract.image_to_string(hand_region, config='--psm 6')  # psm 6 is for sparse text
            if text.strip():
                speak(text)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    return frame

# Open a connection to the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect hand gestures and read text
    frame_with_gesture = detect_gesture_and_read_text(frame)

    # Display the resulting frame
    cv2.imshow('Hand Gesture Detection and Text Reading', frame_with_gesture)

    # Exit the video window when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

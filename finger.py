import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Morse code dictionary
morse_code_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9'
}

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Variables for detecting gestures and Morse code
gesture_start_time = 0
gesture = ""
morse_code = ""
english_text = ""
input_start_time = time.time()
input_duration = 6  # 4 seconds input duration

while cap.isOpened():
    success, img = cap.read()
    if not success:
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Gesture detection logic
            current_time = time.time()
            if current_time - gesture_start_time > 1:  # Detect dash
                if gesture == "dot":
                    morse_code += "."
                elif gesture == "dash":
                    morse_code += "-"
                elif gesture == "space":
                    morse_code += " "  # Add space to separate Morse code letters
                gesture = ""
                gesture_start_time = current_time

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            if index_tip.y < thumb_tip.y and index_tip.y < pinky_tip.y:  # Example condition for dot
                gesture = "dot"
            elif index_tip.y > thumb_tip.y and index_tip.y > pinky_tip.y:  # Example condition for dash
                gesture = "dash"
            elif thumb_tip.y < pinky_tip.y:  # Example condition for space
                gesture = "space"

    # Display the current Morse code and English text
    cv2.putText(img, f"Morse Code: {morse_code}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"English: {english_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Calculate and display the countdown timer
    elapsed_time = time.time() - input_start_time
    remaining_time = max(0, input_duration - elapsed_time)
    cv2.putText(img, f"Time: {remaining_time:.1f}s", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Check if the input duration is over
    if remaining_time == 0:
        # Translate Morse code to English
        morse_letters = morse_code.strip().split(" ")  # Split the morse code by spaces to get individual letters
        for letter in morse_letters:
            if letter in morse_code_dict:
                english_text += morse_code_dict[letter]
            else:
                english_text += " "  # Add space if the Morse code is not recognized
        morse_code = ""
        input_start_time = time.time()  # Reset the input start time for the next input cycle

    cv2.imshow("Morse Code to English", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
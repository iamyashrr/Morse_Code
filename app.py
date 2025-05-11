import streamlit as st
import cv2
import mediapipe as mp
import time
from pydub import AudioSegment
from pydub.generators import Sine
from morse_audio_decoder.morse import MorseCode
import subprocess


st.title("MORSE CODE UTILITY WITH REAL-TIME DETECTION, CONVERSION, AND AUDIO DECODING CAPABILITIES")
st.image("coverpage.png")


st.markdown("### Website Description")
description = """
        <div style='color: grey;'>
        Welcome to the Morse Code Utility website. This project is designed to offer a comprehensive suite of tools for converting text to Morse code, Morse code to text, generating Morse code sounds, and decoding Morse code from audio files. 

        The Morse Code Utility is divided into several functionalities:

        <h4>Text to Morse Code</h4>
        This feature allows you to convert any given text into its corresponding Morse code representation. Simply input your text, and the utility will translate it into Morse code, making it easy for you to communicate in this classic encoding system.

        <h4>Morse Code to Text</h4>
        If you have a Morse code sequence and need to decode it back to text, this tool can help. Just enter the Morse code (with spaces separating the characters), and the utility will provide you with the translated text.

        <h4>Live Morse Code Detection</h4>
        Using advanced computer vision and machine learning techniques, this feature detects Morse code in real-time from a live video feed. This is particularly useful for hands-free communication or for users who prefer to use physical signals to convey their messages.

        <h4>Text to Morse Code Sound</h4>
        This functionality converts text into audible Morse code. It generates a .wav file that plays the Morse code representation of the entered text, allowing you to hear and share Morse code messages easily.

        <h4>Morse Code Audio Decoder</h4>
        Upload an audio file containing Morse code, and the utility will decode the audio back into text. This is helpful for interpreting received Morse code audio signals and translating them into readable text.

        <h4>Technology Stack</h4>
        This project leverages a variety of technologies:
        - <b>Python:</b> The core programming language used for developing the application.
        - <b>Streamlit:</b> Used for building the interactive web interface.
        - <b>OpenCV:</b> Utilized for live video processing and hand gesture detection.
        - <b>MediaPipe:</b> Used for detecting and tracking hand gestures in real-time.
        - <b>Pydub:</b> For generating and manipulating audio files.
        - <b>Morse Audio Decoder:</b> A library used for decoding Morse code from audio files.

        <h4>Project Objectives</h4>
        The main objectives of this project are to:
        - Provide a user-friendly interface for converting between text and Morse code.
        - Enable the generation of Morse code sounds for audio-based communication.
        - Implement live video detection of Morse code using hand gestures.
        - Offer an audio decoding feature to translate Morse code sounds back into text.

        <h4>Future Enhancements</h4>
        We plan to add more features and improve the existing functionalities. Future updates may include:
        - Enhanced live detection with support for multiple hands and more complex gestures.
        - Improved accuracy and speed of the Morse code audio decoder.
        - Additional customization options for Morse code sound generation.
        - Integration with messaging apps for seamless Morse code communication.

        
        """

st.markdown(description, unsafe_allow_html=True)



# Define Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'

}

# Initialize MediaPipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Parameters for Morse code sound
DOT_DURATION = 100  # milliseconds
DASH_DURATION = DOT_DURATION * 3
FREQUENCY = 1000  # Hz for the sine wave

def text_to_morse(text):
    morse_code = ""
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + ' '
        elif char == ' ':
            morse_code += '  '
    return morse_code

def morse_to_sound(morse_code):
    sound = AudioSegment.silent(duration=0)
    for symbol in morse_code:
        if symbol == '.':
            sound += Sine(FREQUENCY).to_audio_segment(duration=DOT_DURATION)
        elif symbol == '-':
            sound += Sine(FREQUENCY).to_audio_segment(duration=DASH_DURATION)
        elif symbol == ' ':
            sound += AudioSegment.silent(duration=DOT_DURATION)  # Intra-character space
        elif symbol == '  ':
            sound += AudioSegment.silent(duration=DOT_DURATION * 7)  # Inter-word space
        # Add a short silence after each dot/dash
        sound += AudioSegment.silent(duration=DOT_DURATION)
    return sound

def text_to_morse_sound(text, output_file):
    morse_code = text_to_morse(text)
    sound = morse_to_sound(morse_code)
    sound.export(output_file, format="wav")

def morse_to_text(morse_code):
    message = ''
    morse_code = morse_code.split(' ')
    for code in morse_code:
        for char, morse in MORSE_CODE_DICT.items():
            if morse == code:
                message += char
    return message

def main():
    st.title("Morse Code Utility")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        app()

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")


from PIL import Image
def app():
    st.sidebar.title("MORE INFO ON MORSE CODE")
    st.sidebar.image("sample.png", use_column_width=True)

    eda_option = st.sidebar.selectbox(
        "MORE INFO ON MORSE CODE",
        ["Select", "Understand Morse Code", "Understand MediaPipe"]
    )

    if eda_option == "Understand Morse Code":
        morse_code_description = """
            Morse code is a method used in telecommunication to encode text characters as standardized sequences of two different signal durations, called dots and dashes. It was named after Samuel Morse, one of the inventors of the telegraph. Each character (letter or numeral) is represented by a unique sequence of dots and dashes. Morse code can be transmitted in various forms, including sound, light, or visual signals.

            Historically, Morse code was used extensively in maritime communication and early radio transmission. It allowed for efficient and clear long-distance communication before the advent of voice radio. Morse code's simplicity and reliability made it an indispensable tool for military, aviation, and emergency services for many years.

            In modern times, while Morse code is no longer widely used in commercial telecommunication, it remains a popular skill among amateur radio operators and is still employed in certain aviation and emergency scenarios. Its enduring legacy is a testament to its effectiveness and the historical importance of long-distance communication.

            The learning of Morse code involves memorizing the distinct patterns of dots and dashes associated with each letter and number, which can be a challenging but rewarding skill. Tools and software for Morse code translation and practice are readily available, helping enthusiasts and professionals keep this communication method alive.
            """
        st.sidebar.image("morsecode.png", use_column_width=True)
        st.sidebar.markdown(morse_code_description)


    elif eda_option == "Understand MediaPipe":
        mediapipe_description = """
            MediaPipe is an open-source framework developed by Google for building cross-platform, customizable ML solutions for live and streaming media. It offers a suite of tools for processing perceptual data, with a particular focus on real-time computer vision and machine learning applications.

            MediaPipe provides pre-built pipelines for tasks such as face detection, hand tracking, pose estimation, and object detection. These pipelines are optimized for performance and can run on various devices, from powerful servers to mobile phones. The framework uses a modular approach, allowing developers to combine and customize different components to fit their specific needs.

            One of the standout features of MediaPipe is its ability to perform real-time processing. For example, the hand tracking solution can detect and track multiple hands simultaneously, providing detailed landmarks for each hand in just a few milliseconds. This makes it highly suitable for applications in augmented reality, interactive media, and gesture-based interfaces.

            Developers using MediaPipe can take advantage of its built-in components or create their own using the framework's extensive APIs. The framework also supports integration with popular machine learning libraries like TensorFlow, making it easier to deploy complex models in real-time applications.

            Overall, MediaPipe is a powerful tool for developers looking to create innovative and efficient media processing applications. Its flexibility, performance, and ease of use have made it a popular choice in both research and industry settings.
            """
        st.sidebar.image("mediapipe.png", use_column_width=True)
        st.sidebar.markdown(mediapipe_description)

    option = st.selectbox(
        "Choose an option",
        ("Text to Morse Code", "Morse Code to Text", "Live Morse Code Detection", "Text to Morse Code Sound", "Morse Code Audio Decoder")
    )

    if option == "Text to Morse Code":
        text = st.text_input("Enter text to convert to Morse code:")
        if text:
            morse_code = text_to_morse(text)
            st.write(f"Morse Code: {morse_code}")

    elif option == "Morse Code to Text":
        morse_code = st.text_input("Enter Morse code to convert to text (use space to separate characters):")
        if morse_code:
            text = morse_to_text(morse_code)
            st.write(f"Text: {text}")

    elif option == "Live Morse Code Detection":
        if st.button("Start Morse Code Detection"):
            subprocess.Popen(["python", "finger.py"])
            st.write("Started Morse Code Detection in a new window.")


    elif option == "Text to Morse Code Sound":
        text = st.text_input("Enter text to convert to Morse code sound:")
        if text:
            output_file = "morse_code_sound.wav"
            text_to_morse_sound(text, output_file)
            st.write(f"Morse code sound for '{text}' has been saved to {output_file}")
            st.audio(output_file)

    elif option == "Morse Code Audio Decoder":
        audio_file = st.file_uploader("Upload a Morse code audio file:", type=["wav"])
        if audio_file:
            with open("uploaded_morse_code.wav", "wb") as f:
                f.write(audio_file.getbuffer())
            morse_code = MorseCode.from_wavfile("uploaded_morse_code.wav")
            text = morse_code.decode()
            st.write(f"Decoded text: {text}")

    st.markdown("""
        <footer style='text-align: center;'>
            <p>&copy; 2024 Your Company. All rights reserved.</p>
        </footer>
        """, unsafe_allow_html=True)

if _name_ == "_main_":
    main()
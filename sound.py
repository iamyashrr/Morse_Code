from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

# Define the Morse code dictionary
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

# Example usage
text = "EWIT"
output_file = "EWIT_morse_code2.wav"
text_to_morse_sound(text, output_file)
print(f"Morse code sound for '{text}' has been saved to {output_file}")



from morse_audio_decoder.morse import MorseCode

morse_code = MorseCode.from_wavfile("EWIT_morse_code2.wav")
out = morse_code.decode()
print(out)
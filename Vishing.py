import pyttsx3
import pyaudio
import numpy as np
import soundfile as sf
import os
import pygame
from tkinter import Tk, Button, filedialog
import shutil  # Ajouté pour la copie de fichiers

# Define constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FOLDER_RECORDING = 'output'
OUTPUT_FOLDER_UPLOADED = 'uploaded'
OUTPUT_FILE_RECORDING = os.path.join(OUTPUT_FOLDER_RECORDING, 'recorded_voice.wav')
OUTPUT_FILE_UPLOADED = os.path.join(OUTPUT_FOLDER_UPLOADED , 'uploaded_audio.wav')


def record_audio(output_file, record_seconds=5):
    """Record audio from microphone and save to file."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    sf.write(output_file, audio_data, RATE)

def upload_audio(output_file):
    """Upload audio file and save to output file using a GUI."""
    def select_file():
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.wav")])
        if file_path:
            shutil.copy(file_path, output_file)
            print(f"Fichier copié : {file_path}")
            root.quit()  # Utilisez root.quit() pour fermer proprement la fenêtre Tkinter

    root = Tk()
    root.title("Upload Audio File")
    Button(root, text="Choisir un fichier audio", command=select_file).pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Gère la fermeture de la fenêtre via le bouton de fermeture
    root.mainloop()
    root.destroy()  # Assurez-vous que la fenêtre est détruite après la fermeture

def play_audio(file_path):
    """Play audio file."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

def main():
    choice = input("Would you like to record your voice (R) or upload an audio file (U)? ").upper()

    if choice == 'R':
        os.makedirs(OUTPUT_FOLDER_RECORDING, exist_ok=True)
        record_audio(OUTPUT_FILE_RECORDING, record_seconds=20)
        output_file = OUTPUT_FILE_RECORDING
    elif choice == 'U':
        os.makedirs(OUTPUT_FOLDER_UPLOADED, exist_ok=True)
        upload_audio(OUTPUT_FILE_UPLOADED)
        output_file = OUTPUT_FILE_UPLOADED
    else:
        print("Invalid choice. Please select 'R' to record or 'U' to upload.")
        return

    play_audio(output_file)

if __name__ == "__main__":
    main()
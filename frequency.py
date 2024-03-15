import librosa
import parselmouth
import numpy as np


import wave


def get_frequency(audio_file):
     # Load audio file
    print(audio_file)
    y, sr = librosa.load(audio_file)

    # Calculate the Fast Fourier Transform (FFT)
    fft = np.abs(librosa.stft(y))

    # Convert FFT to frequency domain
    fft_freqs = librosa.fft_frequencies(sr=sr)

    # Get the peak frequency
    peak_frequency = fft_freqs[np.argmax(np.mean(fft, axis=1))]

    return peak_frequency

audio_file = 'recordings/A.Recording.wav'
frequency = get_frequency(audio_file)
print(f"The dominant frequency of the audio is: {frequency} Hz")


def frequency_wav(recording):
    wav_obj = wave.open(recording, 'rb')
    sample_freq = wav_obj.getframerate()
    print(sample_freq)
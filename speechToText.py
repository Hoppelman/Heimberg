import speech_recognition as sr
import pyaudio
#from transformers import pipeline
import numpy as np

'''recognizer = sr.Recognizer()

print(sr.Microphone())'''

##transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")


def speechToText(tream, new_chunk):
    '''sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
    return stream, transcriber({"sampling_rate": sr, "raw": stream})["text"]'''



    '''print("Test")
    with sr.Microphone() as source:
        audio_data = init_rec.record(source, duration=4)
        print("Recognizing your text.............")
        text = init_rec.recognize_google(audio_data)
        print(text)
        return text

        try:
            # Adjust ambient noise for better recognition
            recognizer.adjust_for_ambient_noise(source)
            
            # Capture audio from the microphone
            audio = recognizer.listen(source, timeout=None)

            print("Transcribing...")

            # Use Google Web Speech API for transcription
            text = recognizer.recognize_google(audio)
            print("Transcription: {}".format(text))

            return text

        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))'''
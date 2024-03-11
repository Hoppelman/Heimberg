from elevenlabs import generate, play, voices, save, clone, stream
from elevenlabs import set_api_key
import shutil
import requests

voiceList = []
voices = voices()
elevenLabs_key = ""

def initElevenLabs(key):
  #set_api_key(api_key)
  global voiceList, elevenLabs_key
  elevenLabs_key = key
  for n in voices.voices:
    if n.category == 'cloned':
        voiceList.append(n.name)
        print(n.voice_id)

  voiceList.append("M.Klon")
  voiceList.append("A.Klon")
  print(voiceList)

def textToSpeech(text, voice_model):
    print("textToSpeech")
    

    if voice_model is None:
       voice_model = voiceList[2]

    audio = generate(
        text=text,
        voice=voice_model,
        model="eleven_multilingual_v2"
    )
    save (
        audio = audio,
        filename = "recordings/outputGPT.wav"
    )
    

    return "recordings/outputGPT.wav"
    


def cloneVoice(recording1, name, description, A_check, M_check):
    print(A_check)
    print(M_check)

    files = [recording1]

    if A_check:
        files.append("recordings/A.Recording.wav")

    if M_check:
        files.append("recordings/M.Recording.wav")

    voice_recording = clone(
        name=name,
        description=description, # Optional
        files=files,
    )
    audio = generate(
        text="Ich bin es, dein Klon.",
        voice=name,
        model="eleven_multilingual_v2"
    )

    save (
        audio = audio,
        filename = "recordings/clone.wav"
    )

    voiceList.append(name)
    print(voiceList)
    initElevenLabs("4dbbe510c74cc81977dab25f205ef7e8")

    #If the name is M.Klon or A.Klon, the recording will be saved for later use
    if name == "M.Klon":
        saveRecording(recording1, "recordings/M.Recording.wav")

    if name == "A.Klon":
        saveRecording(recording1, "recordings/A.Recording.wav")

    return "recordings/clone.wav"



def saveRecording(filePath, fileName):
    with open(filePath, "rb") as file:
            audio_data = file.read()

    with open(fileName, "wb") as file:
        file.write(audio_data)


def generateVoice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/ApxSyhfCtUlzOxkGkSIj"

    payload = {
        "accent": "british",
        "accent_strength": 0.5,
        "age": "middle_aged",
        "gender": "female",
        "text": text
    }

    headers = {
        "xi-api-key": elevenLabs_key,
        "Content-Type": "application/json"
    }

    response_g = requests.request("POST", url, json=payload, headers=headers)
    print(response_g)

    with open('recordings/voiceGeneration.wav', 'wb') as f:
        for chunk in response_g.iter_content(chunk_size=1024):
            if chunk:
                print(chunk)
                f.write(chunk)

    return "recordings/voiceGeneration.wav"

def deleteVoice(name):

    voice_id = None
    for n in voices.voices:
        if n.name == name:
            voice_id = n.voice_id
            print(voice_id)

    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"

    headers = {"xi-api-key": elevenLabs_key}

    response = requests.request("DELETE", url, headers=headers)

    print(response)

def cloneLoop(recording, iterations):
    return ""
    '''
    def generateVoice(text, accent, accent_strength, age, gender):
    API Call for generating voice with model:
    

        url = "https://api.elevenlabs.io/v1/text-to-speech/ApxSyhfCtUlzOxkGkSIj"

    payload = {
        "model_id": "eleven_multilingual_v2",
        "text": "Sag mal, wie geht es dir so?",
        "voice_settings": {
            "similarity_boost": 0.7,
            "stability": 0.7
        }
    }
    headers = {
        "xi-api-key": "4dbbe510c74cc81977dab25f205ef7e8",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    with open('test.wav', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return "test.wav"
    print(response)




    def streamVoice(): 
    audio_stream = generate(
        # api_key="YOUR_API_KEY", (Defaults to os.getenv(ELEVEN_API_KEY))
        text="This is a... streaming voice!!",
        stream=True
    )
    print(audio_stream)
    print(stream(audio_stream))
    '''
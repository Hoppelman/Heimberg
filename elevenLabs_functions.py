from elevenlabs import generate, play, voices, save, clone, stream
from elevenlabs import set_api_key
import shutil
import requests
import librosa
import numpy as np

voiceList = []
myVoices = voices()
elevenLabs_key = ""

def initElevenLabs(key):
  #set_api_key(api_key)
  global voiceList, elevenLabs_key
  elevenLabs_key = key
  updateVoiceList()
  getAccountData()

def updateVoiceList():
    global voiceList, myVoices
    myVoices = voices()
    for n in myVoices.voices:
        if n.category != 'premade':
            voiceList.append(n.name)
    print("Print voiceList: ")
    print(voiceList)

def getVoiceList():
    global voiceList
    voiceList = []
    updateVoiceList()
    return voiceList

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
        filename = "recordings/output.wav"
    )
    
    return "recordings/output.wav"
    
#For cloning the voice. Also called when generating a voice, recording is then the sample generated
def cloneVoice(text, recording, name, description, A_check, M_check, output_check):
    print("cloning....")

    files = []

    if recording is not None:
        files.append(recording)
        #If the name is M.Klon or A.Klon, the recording will be saved for later use
        if name == "M.Klon":
            saveRecording(recording, "recordings/M.Recording.wav")

        if name == "A.Klon":
            saveRecording(recording, "recordings/A.Recording.wav")

    if output_check:
        files.append("recordings/output.wav")

    if A_check:
        files.append("recordings/A.Recording.wav")

    if M_check:
        files.append("recordings/M.Recording.wav")

    clone(
        name=name,
        description=description, # Optional
        files=files,
    )

    print("Voices used for cloning: ")
    print(files)

    audio = generate(
        text=text,
        voice=name,
        model="eleven_multilingual_v2"
    )

    save (
        audio = audio,
        filename = "recordings/output.wav"
    )

    global voiceList
    voiceList = []
    updateVoiceList()

    return "recordings/output.wav"


def saveRecording(filePath, fileName):
    with open(filePath, "rb") as file:
            audio_data = file.read()

    with open(fileName, "wb") as file:
        file.write(audio_data)


def generateVoice(gender, age, accent, accentStrength, text):

    #First we thought the PC was a calculator. Then we found out how to turn numbers into letters and we thought it was a typewriter.
    print("Generating Voice....")
    url = "https://api.elevenlabs.io/v1/voice-generation/generate-voice"

    payload = {
        "accent_strength": accentStrength,
        "accent": accent,
        "age": age,
        "gender": gender,
        "text": text
    }
    headers = {
        "xi-api-key": elevenLabs_key,
        "Content-Type": "application/json"
    }

    response_g = requests.request("POST", url, json=payload, headers=headers)

    print(response_g)

    if response_g.status_code == 200:
        print("Voice successfully created.")
    else:
        print(f"Error creating voice. Status code: {response_g.status_code}")
        try:
            error_message = response_g.json().get("message")
            print(f"Error message: {error_message}")
        except ValueError:
            print("Unable to parse error message from the response.")


    with open('recordings/voiceGeneration.wav', 'wb') as f:
        for chunk in response_g.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    return "recordings/voiceGeneration.wav"

def deleteVoice(name):

    voice_id = None
    for n in myVoices.voices:
        #print(n.name)
        if n.name == name:
            voice_id = n.voice_id
            print("To be deleted voice ID:" + voice_id)

    if voice_id is not None:
        url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"

        headers = {"xi-api-key": elevenLabs_key}

        response = requests.request("DELETE", url, headers=headers)

        if response.status_code == 200:
            print("Voice deleted successfully.")
        else:
            print(f"Error deleting voice. Status code: {response.status_code}")
            try:
                error_message = response.json().get("message")
                print(f"Error message: {error_message}")
            except ValueError:
                print("Unable to parse error message from the response.")

        global voiceList
        voiceList = []
        updateVoiceList()
        print(response)

        return response.status_code
    
    
def getAccountData():
    url = "https://api.elevenlabs.io/v1/user/subscription"

    headers = {"xi-api-key": elevenLabs_key}

    response = requests.request("GET", url, headers=headers)
    print("Remaining voices: " + str(95 - response.json().get("voice_add_edit_counter")))
    return "Remaining voices: " + str(95 - response.json().get("voice_add_edit_counter")) + "\n" + "Remaining characters: " + str(response.json().get("character_limit") - response.json().get("character_count"))



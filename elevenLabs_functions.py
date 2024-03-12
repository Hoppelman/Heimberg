from elevenlabs import generate, play, voices, save, clone, stream
from elevenlabs import set_api_key
import shutil
import requests

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
    #voiceList = []
    for n in myVoices.voices:
        if n.category != 'premade':
            voiceList.append(n.name)
            #print(n.voice_id)
    #voiceList.append("M.Klon")
    #voiceList.append("A.Klon")
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
        filename = "recordings/outputGPT.wav"
    )
    

    return "recordings/outputGPT.wav"
    


def cloneVoice(text, recording, name, description, A_check, M_check, output_check):
    print("cloning....")
    #print("Use A: " + A_check)
    #print("Use M: " + M_check)
    #print("Use recording: " + recording)
    #print("Use generated audio: " + output_check)

    files = []

    if recording is not None:
        files.append(recording)
        #If the name is M.Klon or A.Klon, the recording will be saved for later use
        if name == "M.Klon":
            saveRecording(recording, "recordings/M.Recording.wav")

        if name == "A.Klon":
            saveRecording(recording, "recordings/A.Recording.wav")

    if output_check:
        files.append("recordings/voiceGeneration.wav")

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
        text=text,
        voice=name,
        model="eleven_multilingual_v2"
    )

    save (
        audio = audio,
        filename = "recordings/clone.wav"
    )

    global voiceList
    voiceList = []
    updateVoiceList()
    #initElevenLabs("4dbbe510c74cc81977dab25f205ef7e8")

    return "recordings/clone.wav"


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
        print("Voice deleted successfully.")
    else:
        print(f"Error deleting voice. Status code: {response_g.status_code}")
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

    headers = {"xi-api-key": "4dbbe510c74cc81977dab25f205ef7e8"}

    response = requests.request("GET", url, headers=headers)
    print("Voice edit/add used: " + str(95 - response.json().get("voice_add_edit_counter")))

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
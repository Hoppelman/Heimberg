from elevenlabs import generate, play, voices, save, clone, stream
from elevenlabs import set_api_key

voiceList = []
voices = voices()

def initElevenLabs():
  #set_api_key(api_key)
  global voiceList
  for n in voices.voices:
    if n.category == 'cloned':
        voiceList.append(n.name)

  voiceList.append("M.Klon")
  voiceList.append("A.Klon")
  print(voiceList)

def textToSpeech(text, voice_model):
    if voice_model is None:
       voice_model = voiceList[0]

    audio = generate(
        text=text,
        voice=voice_model,
        model="eleven_multilingual_v2"
    )
    save (
        audio = audio,
        filename = "test.wav"
    )
    return "test.wav"


def cloneVoice(recording1, name, description):
    voice_recording = clone(
        name=name,
        description=description, # Optional
        files=[recording1],
    )
    audio = generate(
        text="Ich bin es, dein Klon.",
        voice=name,
        model="eleven_multilingual_v1"
    )

    fileName = "clone.wav"


    save (
        audio = audio,
        filename = "Clone.wav"
    )

    voiceList.append(name)
    print(voiceList)
    initElevenLabs()

    return fileName

def streamVoice(): 
    audio_stream = generate(
        # api_key="YOUR_API_KEY", (Defaults to os.getenv(ELEVEN_API_KEY))
        text="This is a... streaming voice!!",
        stream=True
    )
    print(audio_stream)
    print(stream(audio_stream))
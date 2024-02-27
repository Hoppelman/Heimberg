from elevenlabs import generate, play, voices, save, clone
from elevenlabs import set_api_key

voiceList = []
voices = voices()

def initElevenLabs(api_key):
  set_api_key(api_key)
  global voiceList
  for n in voices.voices:
    if n.category == 'cloned':
        voiceList.append(n.name)
  print(voiceList)

def textToSpeech(text, voice_model):
    if voice_model is None:
       voice_model = voiceList[0]

    audio = generate(
        text=text,
        voice=voice_model,
        model="eleven_multilingual_v1"
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
        text="Hallo das ist meine geklonte Stimme! Juhuuu!",
        voice=voice_recording,
        model="eleven_multilingual_v1"
    )

    save (
        audio = audio,
        filename = "clone.wav"
    )

    voiceList.append(name)

    return "clone.wav"
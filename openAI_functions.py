from openai import OpenAI
import json

messages = None
client = None

def initOpenAI(api_key, content):
  global client, messages
  client = OpenAI(api_key=api_key)
  messages = [{"role": "system", "content": content}]

def generateText(user_input):
    
  messages.append({"role": "user", "content": user_input})
  print(messages)

  response = client.chat.completions.create(
      messages = messages,
      model = "gpt-3.5-turbo",
  )
  ChatGPT_reply = response.choices[0].message.content

  return ChatGPT_reply

def SpeechToText_File(recording):
  audio_file= open(recording, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
  print(transcription.text)
  return transcription.text
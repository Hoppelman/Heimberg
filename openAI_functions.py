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

    response = client.chat.completions.create(
        messages = messages,
        model = "gpt-3.5-turbo",
    )
    ChatGPT_reply = response.choices[0].message.content

    return ChatGPT_reply


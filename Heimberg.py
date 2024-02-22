import config;
from elevenlabs import generate, play, voices, save, clone
from elevenlabs import set_api_key
set_api_key("4dbbe510c74cc81977dab25f205ef7e8")
import openai
import gradio as gr

openai.api_key = "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"

messages = [{"role": "system", "content": "Du sollst höchstens in 2 Sätzen antworten."}]

voices = voices()
voiceList = []
#cloned_voice = "Rachel"

for n in voices.voices:
    if n.category == 'cloned':
        voiceList.append(n.name)
    
print(voiceList)

def CustomChatGPT(user_input, voice_model):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})


    audio = generate(
        text=ChatGPT_reply,
        voice=voice_model,
        model="eleven_multilingual_v1"
    )
    save (
        audio = audio,
        filename = "test.wav"
    )

    
   # play(audio)
    
    
    return ChatGPT_reply, "test.wav"

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

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines = 4, label = "Frage:")
            text_button = gr.Button("Send")
            with gr.Accordion("Stimme:"): 
                voice_radio = gr.Radio(voiceList, label="Voice")
                with gr.Accordion("Stimme klonen:"): 
                    name_clone = gr.Textbox(label = "Name:")
                    description_clone = gr.Textbox(label = "Beschreibung:")
                    clone_recording1 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                    #clone_recording2 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                    #clone_recording3 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                    klon_button = gr.Button("klonen")
        with gr.Column():
            text_output = gr.Textbox(lines = 4, label = "Antwort:")
            audio_output = gr.Audio(autoplay = True)
            btn_refresh = gr.Button(value="Refresh the page")
            
        
    btn_refresh.click(None, _js="window.location.reload()")
    text_button.click(CustomChatGPT, inputs = [text_input, voice_radio], outputs = [text_output, audio_output])
    klon_button.click(cloneVoice, inputs = [clone_recording1, name_clone, description_clone], outputs = [audio_output])

demo.launch(share=True)

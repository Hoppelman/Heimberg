import json;
from elevenlabs import clone
from elevenlabs import set_api_key

with open('config.json') as f:
    config = json.load(f)

set_api_key(config['elevenLabs_key'])


from openAI_functions import initOpenAI, generateText
from elevenLabs_functions import initElevenLabs, textToSpeech, cloneVoice, voiceList
import gradio as gr


initOpenAI(config['api_key'], "Du sollst höchstens in 2 Wörtern antworten.")
initElevenLabs()


def getAnswerWithVoice(user_input, voice_model):
    text = generateText(user_input)
    outputFile = textToSpeech(text, voice_model)
    #outputFile = "test.wav"
    return text, outputFile

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
                    clone_recording1 = gr.Audio(sources="microphone", type = "filepath", format = "mp3")
                    #clone_recording2 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                    #clone_recording3 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                    klon_button = gr.Button("klonen")
        with gr.Column():
            text_output = gr.Textbox(lines = 4, label = "Antwort:")
            audio_output = gr.Audio(autoplay = True)
            btn_refresh = gr.Button(value="Refresh the page")
            
        
    #btn_refresh.click(None, _js="window.location.reload()")
    text_button.click(getAnswerWithVoice, inputs = [text_input, voice_radio], outputs = [text_output, audio_output])
    klon_button.click(cloneVoice, inputs = [clone_recording1, name_clone, description_clone], outputs = [audio_output])

demo.launch(share=True)

import json;
from elevenlabs import clone
from elevenlabs import set_api_key

with open('config.json') as f:
    config = json.load(f)

set_api_key(config['elevenLabs_key'])

from openAI_functions import initOpenAI, generateText
from elevenLabs_functions import initElevenLabs, textToSpeech, cloneVoice, voiceList, generateVoice, deleteVoice
from speechToText import speechToText
import gradio as gr

initOpenAI(config['api_key'], "")
initElevenLabs(config['elevenLabs_key'])


def getAnswerWithVoice(user_input, voice_model):
    text = generateText(user_input)
    outputFile = textToSpeech(text, voice_model)
    print(voice_model)
    #outputFile = "test.wav"
    return text, outputFile


with gr.Blocks(theme= gr.themes.Base(), js="speechToText.js") as demo:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines = 4, label = "Frage:")
            with gr.Accordion("Stimme:"): 
                with gr.Tab("Stimme"):
                    voice_radio = gr.Radio(voiceList, label="Voice")
                    delete_voice_button = gr.Button(value = "Stimme löschen", size = 2)
                with gr.Tab("Stimme generieren"):
                    generateVoice_button = gr.Button("Künstliche Stimme generieren")
            GPT_button = gr.Button("Generiere GPT Response")
            onlyText_button = gr.Button("Nur Text to Speech")
            with gr.Accordion("Stimme klonen:"): 
                name_clone = gr.Dropdown(["A.Klon", "M.Klon"], label="Name:", allow_custom_value = True)
                description_clone = gr.Textbox(label = "Beschreibung:")
                clone_recording1 = gr.Audio(sources="microphone", type = "filepath", format = "mp3")
                A_check = gr.Checkbox(label="A.Recording", info="Nutze das A. Recording zum Klonen")
                M_check = gr.Checkbox(label="M.Recording", info="Nutze das M. Recording zum Klonen")
                #clone_recording2 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                #clone_recording3 = gr.Audio(source="microphone", type = "filepath", format = "mp3")
                klon_button = gr.Button("klonen")
        with gr.Column():
            text_output = gr.Textbox(lines = 4, label = "Antwort:")
            audio_output = gr.Audio(autoplay = False)
            with gr.Row():
                with gr.Accordion("Speech To Text:"): 
                    speechToText_Output = gr.Textbox(lines = 5, label = "", elem_id="speechToText_output")
                    speechToText_Recorder = gr.Audio(sources="microphone", streaming = True)
            
    #Events
    GPT_button.click(
        getAnswerWithVoice, 
        inputs = [text_input, voice_radio], 
        outputs = [text_output, audio_output]
    )

    onlyText_button.click(
        textToSpeech, 
        inputs = [text_input, voice_radio], 
        outputs = [audio_output]
    )

    generateVoice_button.click(
        generateVoice,
        inputs = [text_input],
        outputs = [audio_output]
    )

    klon_button.click(
        cloneVoice, 
        inputs = [clone_recording1, name_clone, description_clone, A_check, M_check], 
        outputs = [audio_output]
    )

    
    delete_voice_button.click(
        deleteVoice,
        inputs = [voice_radio]
    )
    

    '''speechToText_Recorder.stream(
        speechToText,
        outputs = ["state", speechToText_Output]
    )'''

    live = True


demo.launch(share=False)

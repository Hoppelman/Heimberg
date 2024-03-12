import json;
import time;
from elevenlabs import clone
from elevenlabs import set_api_key

with open('config.json') as f:
    config = json.load(f)

set_api_key(config['elevenLabs_key'])

from openAI_functions import initOpenAI, generateText
from elevenLabs_functions import initElevenLabs, textToSpeech, cloneVoice, voiceList, generateVoice, deleteVoice, updateVoiceList, getVoiceList
import gradio as gr

initOpenAI(config['api_key'], "Antworte maximal in 4 Sätzen.")
initElevenLabs(config['elevenLabs_key'])


def getAnswerWithVoice(user_input, voice_model):
    
    text = generateText(user_input)
    outputFile = textToSpeech(text, voice_model)
    print(voice_model)
    return text, outputFile


def press_reloadButton():
    print(voiceList)
    return gr.Radio(getVoiceList(), label="Voice", every = 1)

def press_deleteButton(voice_name): 
    deleteVoice(voice_name)
    return gr.Radio(getVoiceList(), label="Voice", every=1)

def press_cloneButton(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check): 
    audio_response = cloneVoice(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check)
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1)

def press_generateButton(name, gender, age, accent, accentStrength, text):
    print("GenerateButton")
    voice_sample = generateVoice(gender, age, accent, accentStrength, text)
    return voice_sample, gr.Radio(getVoiceList(), label="Voice", every=1)


with gr.Blocks(theme= gr.themes.Base(), js="speechToText.js") as demo:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines = 4, label = "Eingabe:")
            with gr.Accordion("Stimme:"): 
                with gr.Tab("Stimme auswählen"):
                    voice_radio = gr.Radio(voiceList, label="Voice", every = 1)
                    delete_voice_button = gr.Button(value = "Stimme löschen", size = 2)
                    reload_button = gr.Button(value = "Stimmen laden", size = 2)
                    onlyText_button = gr.Button("Text to Speech")
                    GPT_button = gr.Button("Generiere GPT Response")
                with gr.Tab("Stimme generieren"):
                    name_generate = gr.Textbox(label = "Name:")
                    gender_generate = gr.Dropdown(["male", "female"], label="Geschlecht:", allow_custom_value = False)
                    age_generate = gr.Dropdown(["young", "middle_aged", "old"], label="Alter:", allow_custom_value = False)
                    accent_generate = gr.Dropdown(["american", "british"], label="Akzent:", allow_custom_value = False)
                    accentStrength_generate = gr.Slider(0.3, 2.0, step=0.1, label='Akzentstärke:', value=0.5, interactive=True)
                    generateVoice_button = gr.Button("Künstliche Stimme generieren")
                with gr.Tab("Stimme klonen"):
                    name_clone = gr.Dropdown(["A.Klon", "M.Klon"], label="Name:", allow_custom_value = True)
                    description_clone = gr.Textbox(label = "Beschreibung:")
                    clone_recording1 = gr.Audio(sources="microphone", type = "filepath", format = "mp3")
                    A_check = gr.Checkbox(label="A.Recording", info="Nutze das A. Recording zum Klonen")
                    M_check = gr.Checkbox(label="M.Recording", info="Nutze das M. Recording zum Klonen")
                    output_check = gr.Checkbox(label="Audio Output", info="Nutze generiertes Audio zum Klonen")
                    klon_button = gr.Button("klonen")
        with gr.Column():
            text_output = gr.Textbox(lines = 4, label = "Antwort:")
            audio_output = gr.Audio(autoplay = False)
            with gr.Row():
                with gr.Accordion("Speech To Text:"): 
                    speechToText_Output = gr.Textbox(lines = 5, label = "", elem_id="speechToText_output", autoscroll = True)
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
        press_generateButton,
        inputs = [name_generate, gender_generate, age_generate, accent_generate, accentStrength_generate, text_input],
        outputs = [audio_output, voice_radio]
    )

    klon_button.click(
        press_cloneButton, 
        inputs = [text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check], 
        outputs = [audio_output, voice_radio]
    )

    delete_voice_button.click(
        press_deleteButton,
        inputs = [voice_radio],
        outputs = [voice_radio]
    )
    
    reload_button.click(press_reloadButton, None, voice_radio)

    live = True


demo.launch(share=False)

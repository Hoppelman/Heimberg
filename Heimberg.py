import json;
import time;
from elevenlabs import clone
from elevenlabs import set_api_key
import os
from frequency import frequency_wav, get_frequency

with open('config.json') as f:
    config = json.load(f)

set_api_key(config['elevenLabs_key'])

from openAI_functions import initOpenAI, generateText, SpeechToText_File
from elevenLabs_functions import initElevenLabs, textToSpeech, cloneVoice, voiceList, generateVoice, deleteVoice, getVoiceList, getAccountData
from templateData import templateData
import gradio as gr

initOpenAI(config['api_key'], "Antworte maximal in 4 Sätzen.")
initElevenLabs(config['elevenLabs_key'])

textTemplates = list(templateData.keys())

def getAnswerWithVoice(user_input, voice_model):
    if user_input in textTemplates:
        if templateData[user_input] is not None and isinstance(templateData[user_input], tuple):
            time.sleep(2)
            return templateData[user_input][0], templateData[user_input][1]
    text = generateText(user_input)
    outputFile = textToSpeech(text, voice_model)
    print(voice_model)
    return text, outputFile

def press_onlyText_button(user_input, voice_model):
    if user_input in textTemplates:
        if templateData[user_input] is not None and isinstance(templateData[user_input], str):
            time.sleep(2)
            return templateData[user_input]
    ouputFile = textToSpeech(user_input, voice_model)
    return ouputFile

def press_reloadButton():
    print(voiceList)
    return gr.Radio(getVoiceList(), label="Voice", every = 1), gr.Textbox(getAccountData(), lines = 1, show_label = False)

def press_reloadRemainButton():
    return gr.Textbox(getAccountData(), lines = 1, show_label = False)

def press_deleteButton(voice_name): 
    deleteVoice(voice_name)
    return gr.Radio(getVoiceList(), label="Voice", every=1)

def press_cloneButton(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check): 
    audio_response = cloneVoice(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check)
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1)

def press_generateButton(name, gender, age, accent, accentStrength, text, description):
    print("GenerateButton")
    generate_text = "First we thought the PC was a calculator. Then we found out how to turn numbers into letters and we thought it was a typewriter."
    voice_sample = generateVoice(gender, age, accent, accentStrength, generate_text)
    audio_response = cloneVoice(text, voice_sample, name, description, False, False, False)
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1)

def stop_SpeechToTextRecording(recording):
    text = SpeechToText_File(recording)
    return text


with gr.Blocks(theme= gr.themes.Base(), js="speechToText.js") as Anrede1:
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines = 4, label = "Eingabe:")
            with gr.Accordion("Vorlagen:"): 
                gr.Examples(
                    textTemplates,
                    [text_input]
            )
            with gr.Accordion("Stimme:"): 
                with gr.Tab("Stimme auswählen"):
                    voice_radio = gr.Radio(voiceList, show_label = False, every = 1)
                    delete_voice_button = gr.Button(value = "Stimme löschen", size = 2)
                    reload_button = gr.Button(value = "Stimmen laden", size = 2)
                    onlyText_button = gr.Button("Text to Speech")
                    GPT_button = gr.Button("Generiere GPT Response")
                with gr.Tab("Stimme generieren"):
                    name_generate = gr.Textbox(label = "Name:")
                    gender_generate = gr.Dropdown(["male", "female"], label="Geschlecht:", allow_custom_value = False)
                    age_generate = gr.Dropdown(["young", "middle_aged", "old"], label="Alter:", allow_custom_value = False)
                    description_generate = gr.Textbox(label = "Beschreibung:")
                    accent_generate = gr.Dropdown(["american", "british"], label="Akzent:", allow_custom_value = False)
                    accentStrength_generate = gr.Slider(0.3, 2.0, step=0.1, label='Akzentstärke:', value=0.5, interactive=True)
                    generateVoice_button = gr.Button("Künstliche Stimme generieren")
                with gr.Tab("Stimme klonen"):
                    name_clone = gr.Dropdown(["A.Klon", "M.Klon"], label="Name:", allow_custom_value = True)
                    description_clone = gr.Textbox(label = "Beschreibung:")
                    clone_recording1 = gr.Audio(sources="microphone", type = "filepath", format = "wav")
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
                    speechToTextQuestion_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Frage stellen")
                    #waveform = gr.make_waveform("recordings/A.Recording.wav")
                    #video_Waveform = gr.Video(gr.make_waveform("recordings/A.Recording.wav", bar_count = 140, animate=True))
            with gr.Row():
                with gr.Accordion("Hertztester:"):
                    frequency_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Aufnahme starten")
                    frequency_Output = gr.Textbox(lines = 1, label = "Hertz: ")
            with gr.Row():
                with gr.Accordion("Account:"):
                    ramainingVoices = gr.Textbox(getAccountData, lines = 1, show_label = False)
                    reloadRemaining_button = gr.Button("Refresh")

    #Events
    GPT_button.click(
        getAnswerWithVoice, 
        inputs = [text_input, voice_radio], 
        outputs = [text_output, audio_output]
    )

    onlyText_button.click(
        press_onlyText_button, 
        inputs = [text_input, voice_radio], 
        outputs = [audio_output]
    )

    generateVoice_button.click(
        press_generateButton,
        inputs = [name_generate, gender_generate, age_generate, accent_generate, accentStrength_generate, text_input, description_generate],
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
    
    reload_button.click(press_reloadButton, None, outputs = [voice_radio])

    reloadRemaining_button.click(
        press_reloadRemainButton,
        None,
        outputs = ramainingVoices
    )

    speechToTextQuestion_Audio.stop_recording(
        stop_SpeechToTextRecording,
        speechToTextQuestion_Audio,
        text_input
    )

    frequency_Audio.stop_recording(
        get_frequency,
        frequency_Audio,
        frequency_Output
    )


live = True

Eustachius = gr.load(
    "huggingface/facebook/wav2vec2-base-960h",
    title=None,
    inputs=gr.Microphone(type="filepath"),
    description="Let me try to guess what you're saying!",
)

with gr.Blocks(theme= gr.themes.Base(), js="speechToText.js") as Heimberg:
    text_input = gr.Textbox(lines = 4, label = "Eingabe:")

demo = gr.TabbedInterface([Anrede1, Eustachius, Heimberg], ["Anrede1", "Eustachius", "Heimberg"])

demo.launch(share=False)

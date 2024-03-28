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

initOpenAI(config['api_key'], "Antworte in maximal 200 Zeichen, inklusive Leerzeichen.")
initElevenLabs(config['elevenLabs_key'])

textTemplates = list(templateData.keys())

theme = gr.themes.Monochrome(
    text_size="lg",
)

def js_to_prefere_the_back_camera_of_mobilephones():
    custom_html = """
    <script>
    const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);

    navigator.mediaDevices.getUserMedia = async (constraints) => {
    try {
        if (constraints.video && !constraints.video.deviceId) {
            console.log("Head skript3")
            // Check if constraints.video is defined and if deviceId is not set
            // Get list of available media devices
            const devices = await navigator.mediaDevices.enumerateDevices();

            // Find the USB-C camera by checking its label or kind
            const usbCCamera = devices.find(device => 
                device.kind === 'videoinput' && 
                (device.label.includes('USB-Kamera') || device.label.includes('USB-Kamera (0bda:0521)'))
            );
            console.log(devices)
            console.log(usbCCamera)
            console.log("deviceID: " + usbCCamera.deviceId)
            // If USB-C camera is found, set its deviceId in the constraints
            if (usbCCamera) {
                constraints.video.deviceId = usbCCamera.deviceId;
            }
        }
            
        // Call the original getUserMedia with modified constraints
        return await originalGetUserMedia(constraints);
    } catch (error) {
        // Handle errors
        console.error('Error accessing media devices:', error);
        throw error;
    }
    };
    </script>
    """
    return custom_html

def heimberg_stop_SpeechToTextRecording(recording): 
    text = SpeechToText_File(recording)
    audio_output = "recordings/preRecorded/Heimberg/heimberg_GPT.mp3"
    return text, gr.Audio(autoplay = True, value = audio_output, visible = True)

def stimmuntersuchung_stop_SpeechToTextRecording(recording): 
    text = SpeechToText_File(recording)
    return text

def anrede_2_stop_SpeechToTextRecording(recording): 
    text = SpeechToText_File(recording)
    return text


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
            time.sleep(3)
            return templateData[user_input]
    ouputFile = textToSpeech(user_input, voice_model)
    return ouputFile

def press_reloadButton():
    print(voiceList)
    return gr.Radio(getVoiceList(), label="Voice", every = 1)

def press_reloadRemainButton():
    return gr.Textbox(getAccountData(), lines = 1, show_label = False)

def press_deleteButton(voice_name): 
    deleteVoice(voice_name)
    return gr.Radio(getVoiceList(), label="Voice", every=1)

'''
def press_cloneButton(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check): 
    audio_response = cloneVoice(text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check)
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1)
'''
def press_cloneButton(text_input, clone_recording1, name_clone, description_clone): 
    audio_response = cloneVoice(text_input, clone_recording1, name_clone, description_clone)
    if(audio_response == "recording_missing"):
        return None
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1), gr.Radio(getVoiceList(), label="Voice", every=1)

def press_generateButton(name, gender, age, accent, accentStrength, text, description):
    print("GenerateButton")
    #audio_response = "recordings/output.wav"
    #time.sleep(3)
    generate_text = "First we thought the PC was a calculator. Then we found out how to turn numbers into letters and we thought it was a typewriter."
    voice_sample = generateVoice(gender, age, accent, accentStrength, generate_text)
    audio_response = cloneVoice(text, voice_sample, name, description, False, False, False)
    return audio_response, gr.Radio(getVoiceList(), label="Voice", every=1)

def stop_SpeechToTextRecording(recording):
    text = SpeechToText_File(recording)
    return text

def showLoadingAnimation_T2S():
    print("Test")
    return gr.Gallery(
        value = ["media/Telefonistin/Telefonistin.gif", "media/Telefonistin/Telefonistin6.gif", "media/Telefonistin/Telefonistin.gif"],
        visible = True, label="Generated images", show_label=False, elem_id="gallery"
        , columns=[3], rows=[1], object_fit="contain", height="auto"
        )

def showLoadingAnimation_Generate():
    print("Generate_Loading_Animation")
    return gr.Gallery(
        value = ["media/MRI/MRI1.gif", "media/VocalCords/Voice.gif", "media/MRI/MRI3.gif"],
        visible = True, label="Generated images", show_label=False, elem_id="gallery"
        , columns=[3], rows=[1], object_fit="contain", height="auto"
        )

def hideLoadingAnimation():
    return gr.Gallery(
        value = ["media/Telefonistin/Telefonistin.gif", "media/Telefonistin/Telefonistin6.gif", "media/Telefonistin/Telefonistin.gif"],
        visible = False, label="Generated images", show_label=False, elem_id="gallery"
        , columns=[3], rows=[1], object_fit="contain", height="auto"
        )


#head=js_to_prefere_the_back_camera_of_mobilephones()
with gr.Blocks(js="speechToText.js", head=js_to_prefere_the_back_camera_of_mobilephones()) as demo:

    with gr.Tab("Anrede 1", elem_id = "Anrede 1"):
        anrede_1_titleCard_video = gr.Video(value = "media/TitleCards/Anrede_1_titleCard.mp4", autoplay = True, elem_id = "Anrede 1_titleCard-Video", show_label = False, show_download_button = False, visible=False)

    with gr.Tab("Heimberg", elem_id = "Heimberg"): 
        #heimberg_title = gr.Label(value = "Heimberg")
        heimberg_titleCard_video = gr.Video(value = "media/TitleCards/Heimberg_titleCard.mp4", autoplay = True, elem_id = "Heimberg_titleCard-Video", show_label = False, show_download_button = False)
        #heimberg_title_card = gr.Image(value = "media/TitleCards/Heimberg.png", show_download_button = False, show_label = False, elem_id = "Heimberg-titleCard")
        heimber_webcam = gr.Image(streaming = True, elem_id = "Heimberg-webcam")
        heimberg_titleCard_video = gr.Video(value = "media/Heimberg/Schweigen.mp4", autoplay = True, visible=False, elem_id = "Heimberg_Schweigen-Video", show_label = False, show_download_button = False)
        heimberg_text_input = gr.Textbox(lines = 4, value = "", show_label = False, elem_id="heimberg_textbox")
        heimberg_audio_output = gr.Audio(autoplay = False, visible = False)
        heimberg_speechToTextQuestion_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Frage stellen")
        

    with gr.Tab("Ratgeber Hausfrau", elem_id = "Ratgeber Hausfrau"):
        ratgeber_hausfrau_titleCard_video = gr.Video(value = "media/TitleCards/Ratgeber_Hausfrau_titleCard.mp4", autoplay = True, elem_id = "Ratgeber Hausfrau_titleCard-Video", show_label = False, show_download_button = False)
        ratgeber_hausfrau_video = gr.Video(value = "media/Ratgeber_Hausfrau/Ratgeber_Hausfrau.mp4", autoplay = True, elem_id = "Ratgeber Hausfrau-Video", show_label = False, show_download_button = False)

    with gr.Tab("Erfahrungen", elem_id = "Erfahrungen"):
        erfahrungen_titleCard_video = gr.Video(value = "media/TitleCards/Erfahrungen_titleCard.mp4", autoplay = True, elem_id = "Erfahrungen_titleCard-Video", show_label = False, show_download_button = False)

    with gr.Tab("Stimmuntersuchung", elem_id = "Stimmuntersuchung"):
        stimmuntersuchung_video = gr.Video(value = "media/TitleCards/Stimmuntersuchung_titleCard.mp4", autoplay = True, elem_id = "Stimmuntersuchung_titleCard-Video", show_label = False, show_download_button = False)
        stimmuntersuchung_webcam = gr.Image(streaming = True, elem_id = "Stimmuntersuchung-webcam")
        with gr.Row():
            with gr.Column():
                stimmuntersuchung_text_input = gr.Textbox(lines = 4, value = "", show_label = False, elem_id="stimmuntersuchung_textbox")
                stimmuntersuchung_speechToTextQuestion_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Frage stellen")
                #speechToTextQuestion_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Frage stellen")
                with gr.Accordion("Vorlagen:"): 
                    gr.Examples(
                        textTemplates,
                        [stimmuntersuchung_text_input]
                )
                with gr.Accordion("Stimme:"): 
                    with gr.Tab("Stimme auswählen"):
                        stimmuntersuchung_voice_radio = gr.Radio(voiceList, show_label = False, every = 1)
                        #delete_voice_button = gr.Button(value = "Stimme löschen", size = 2)
                        stimmuntersuchung_reload_button = gr.Button(value = "Stimmen laden", size = 2)
                        stimmuntersuchung_onlyText_button = gr.Button("Text to Speech")
                        stimmuntersuchung_GPT_button = gr.Button("Generiere GPT Response")
                    '''with gr.Tab("Stimme generieren"):
                        name_generate = gr.Textbox(label = "Name:")
                        gender_generate = gr.Dropdown(["male", "female"], label="Geschlecht:", allow_custom_value = False)
                        age_generate = gr.Dropdown(["young", "middle_aged", "old"], label="Alter:", allow_custom_value = False)
                        description_generate = gr.Textbox(label = "Beschreibung:")
                        accent_generate = gr.Dropdown(["american", "british"], label="Akzent:", allow_custom_value = False)
                        accentStrength_generate = gr.Slider(0.3, 2.0, step=0.1, label='Akzentstärke:', value=0.5, interactive=True)
                        generateVoice_button = gr.Button("Künstliche Stimme generieren")'''
                    with gr.Tab("Stimme klonen"):
                        name_clone = gr.Dropdown(["A.Klon", "M.Klon"], label="Name:", allow_custom_value = True)
                        description_clone = gr.Textbox(label = "Beschreibung:")
                        clone_recording1 = gr.Audio(sources="microphone", type = "filepath", format = "wav")
                        #A_check = gr.Checkbox(label="A.Recording", info="Nutze das A. Recording zum Klonen")
                        #M_check = gr.Checkbox(label="M.Recording", info="Nutze das M. Recording zum Klonen")
                        #output_check = gr.Checkbox(label="Audio Output", info="Nutze generiertes Audio zum Klonen")
                        klon_button = gr.Button("klonen")
            with gr.Column():
                stimmuntersuchung_text_output = gr.Textbox(lines = 4, label = "Antwort:")
                stimmuntersuchung_audio_output = gr.Audio(autoplay = False)
                stimmuntersuchung_output_gallery = gr.Gallery(
                            value = ["media/Telefonistin/Telefonistin.gif", "media/Telefonistin/Telefonistin6.gif", "media/Telefonistin/Telefonistin.gif"],
                            visible = False, label="Generated images", show_label=False, elem_id="gallery"
                            , columns=[3], rows=[1], object_fit="contain", height="auto"
                        )
                '''with gr.Row():
                    with gr.Accordion("Hertztester:"):
                        frequency_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Aufnahme starten")
                        frequency_Output = gr.Textbox(lines = 1, label = "Hertz: ")'''
                '''with gr.Row():
                    with gr.Accordion("Account:"):
                        ramainingVoices = gr.Textbox(getAccountData, lines = 1, show_label = False)
                        reloadRemaining_button = gr.Button("Refresh")'''
                
    with gr.Tab("Anrede 2", elem_id = "Anrede_2"):
        anrede_2_titleCard_video = gr.Video(value = "media/TitleCards/Anrede_2_titleCard.mp4", autoplay = True, elem_id = "Anrede 2_titleCard-Video", show_label = False, show_download_button = False)
        with gr.Row():
            with gr.Column():
                anrede_2_text_input = gr.Textbox(lines = 4, value = "", show_label = False, elem_id="anrede 2_textbox")
                anrede_2_speechToTextQuestion_Audio = gr.Audio(sources="microphone", type = "filepath", format = "wav", label = "Frage stellen")
                with gr.Accordion("Stimme:"): 
                    anrede_2_voice_radio = gr.Radio(voiceList, show_label = False, every = 1)
                    anrede_2_reload_button = gr.Button(value = "Stimmen laden", size = 2)
                    anrede_2_onlyText_button = gr.Button("Text to Speech")
                    anrede_2_GPT_button = gr.Button("Generiere GPT Response")
            with gr.Column():
                anrede_2_text_output = gr.Textbox(lines = 4, label = "Antwort:")
                anrede_2_audio_output = gr.Audio(autoplay = False, interactive = False)
                anrede_2_output_gallery = gr.Gallery(
                            value = ["media/Telefonistin/Telefonistin.gif", "media/Telefonistin/Telefonistin6.gif", "media/Telefonistin/Telefonistin.gif"],
                            visible = False, label="Generated images", show_label=False, elem_id="gallery"
                            , columns=[3], rows=[1], object_fit="contain", height="auto"
                        )
                
    with gr.Tab("Trigger", elem_id = "Trigger"):
        trigger_titleCard_video = gr.Video(value = "media/TitleCards/Trigger_titleCard.mp4", autoplay = True, elem_id = "Trigger_titleCard-Video", show_label = False, show_download_button = False)
        speechToText_Output = gr.Textbox(lines = 15, show_label = False, elem_id="speechToText_output_trigger", autoscroll = True)
        trigger_video = gr.Video(value = "media/Trigger/Vocal_cords.mp4", autoplay = True, elem_id = "Trigger-Video", show_label = False, show_download_button = False)

    with gr.Tab("Gedicht", elem_id = "Gedicht"):
        gedicht_titleCard_video = gr.Video(value = "media/TitleCards/Gedicht_titleCard.mp4", autoplay = True, elem_id = "Gedicht_titleCard-Video", show_label = False, show_download_button = False)

    with gr.Tab("Glimmer", elem_id = "Glimmer"):
        glimmer_titleCard_video = gr.Video(value = "media/TitleCards/Glimmer_titleCard.mp4", autoplay = True, elem_id = "Glimmer_titleCard-Video", show_label = False, show_download_button = False)
        speechToText_Output = gr.Textbox(lines = 15, show_label = False, elem_id="speechToText_output_glimmer", autoscroll = True)
        glimmer_video = gr.Video(value = "media/Glimmer/Vocal_cords.mp4", autoplay = True, elem_id = "Glimmer-Video", show_label = False, show_download_button = False)


    #Heimberg
    heimberg_speechToTextQuestion_Audio.stop_recording(
        heimberg_stop_SpeechToTextRecording,
        inputs = [heimberg_speechToTextQuestion_Audio],
        outputs = [heimberg_text_input, heimberg_audio_output]
    )

    #Anrede 2
    anrede_2_speechToTextQuestion_Audio.stop_recording(
        anrede_2_stop_SpeechToTextRecording,
        inputs = [anrede_2_speechToTextQuestion_Audio],
        outputs = [anrede_2_text_input]
    )

    anrede_2_GPT_button.click(
        getAnswerWithVoice, 
        inputs = [anrede_2_text_input, anrede_2_voice_radio], 
        outputs = [anrede_2_text_output, anrede_2_audio_output]
    )

    anrede_2_onlyText_button.click(
        press_onlyText_button, 
        inputs = [anrede_2_text_input, anrede_2_voice_radio], 
        outputs = [anrede_2_audio_output]
    )

    #Stimmuntersuchung
    stimmuntersuchung_speechToTextQuestion_Audio.stop_recording(
        stimmuntersuchung_stop_SpeechToTextRecording,
        inputs = [stimmuntersuchung_speechToTextQuestion_Audio],
        outputs = [stimmuntersuchung_text_input]
    )

    stimmuntersuchung_GPT_button.click(
        getAnswerWithVoice, 
        inputs = [stimmuntersuchung_text_input, stimmuntersuchung_voice_radio], 
        outputs = [stimmuntersuchung_text_output, stimmuntersuchung_audio_output]
    )

    stimmuntersuchung_onlyText_button.click(
        press_onlyText_button, 
        inputs = [stimmuntersuchung_text_input, stimmuntersuchung_voice_radio], 
        outputs = [stimmuntersuchung_audio_output]
    )

    stimmuntersuchung_onlyText_button.click(
        showLoadingAnimation_T2S, 
        None, 
        outputs = [stimmuntersuchung_output_gallery]
    )

    stimmuntersuchung_audio_output.change(
        hideLoadingAnimation,
        None,
        outputs = [stimmuntersuchung_output_gallery]
    )

    

    '''generateVoice_button.click(
        press_generateButton,
        inputs = [name_generate, gender_generate, age_generate, accent_generate, accentStrength_generate, text_input, description_generate],
        outputs = [audio_output, voice_radio]
    )

    generateVoice_button.click(
        showLoadingAnimation_Generate,
        None,
        outputs = [output_gallery]
    )'''

    klon_button.click(
        showLoadingAnimation_Generate,
        None,
        outputs = [stimmuntersuchung_output_gallery]
    )

    '''
    klon_button.click(
        press_cloneButton, 
        inputs = [text_input, clone_recording1, name_clone, description_clone, A_check, M_check, output_check], 
        outputs = [audio_output, voice_radio]
    )'''

    klon_button.click(
        press_cloneButton, 
        inputs = [stimmuntersuchung_text_input, clone_recording1, name_clone, description_clone], 
        outputs = [stimmuntersuchung_audio_output, stimmuntersuchung_voice_radio, anrede_2_voice_radio]
    )

    klon_button.click(
        showLoadingAnimation_Generate,
        None,
        outputs = [stimmuntersuchung_output_gallery]
    )

    '''delete_voice_button.click(
        press_deleteButton,
        inputs = [voice_radio],
        outputs = [voice_radio]
    )'''
    
    stimmuntersuchung_reload_button.click(press_reloadButton, None, outputs = [stimmuntersuchung_voice_radio])

    '''reloadRemaining_button.click(
        press_reloadRemainButton,
        None,
        outputs = ramainingVoices
    )'''

    '''speechToTextQuestion_Audio.stop_recording(
        stop_SpeechToTextRecording,
        speechToTextQuestion_Audio,
        text_input
    )


    frequency_Audio.stop_recording(
        get_frequency,
        frequency_Audio,
        frequency_Output
    )'''


live = True

demo.launch(share=False)

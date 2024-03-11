

function textToSpeech() {

    var containerDiv = document.getElementById('speechToText_output');
    var textarea = containerDiv.querySelector('[data-testid="textbox"]');
    console.log(textarea);
    let output_text = textarea.value;
    //textarea.value = output_text;

    window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

    textbox = document.getElementById("speechToText_output");
    console.log(textbox);

    const recognition = new SpeechRecognition();
    console.log(recognition);
    recognition.interimResults = false;
    let state = "sleep";

    recognition.addEventListener("result", (e) => {
        let text = Array.from(e.results)
            .map((result) => result[0])
            .map((result) => result.transcript)
            .join("");

        console.log(text);
        if (e.results[0].isFinal) {
            //text = text.toLowerCase();
            console.log(text);
            output_text = output_text + " \n" + text;
            textarea.value = output_text;
            

        }
    });

    recognition.addEventListener("end", () => {
        if(state === 'sleep') {
            recognition.start();
        }
    });

    recognition.start();
}


function textToSpeech() {
    console.log("Js is loaded")
    var containerDiv_G = document.getElementById('speechToText_output_glimmer');
    var containerDiv_T = document.getElementById('speechToText_output_trigger');
    var containerDiv_H = document.getElementById('heimberg_textbox');
    var textarea_G = containerDiv_G.querySelector('[data-testid="textbox"]');
    var textarea_T = containerDiv_T.querySelector('[data-testid="textbox"]');
    var textarea_H = containerDiv_H.querySelector('[data-testid="textbox"]');
    console.log(textarea_G);
    let output_text = textarea_G.value;
    let currentText = "";
    //textarea.value = output_text;

    window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

    textbox = document.getElementById("speechToText_output");
    console.log("Js is loaded")
    console.log(textarea_G);

    const recognition = new SpeechRecognition();
    console.log(recognition);
    recognition.interimResults = true;
    let state = "sleep";

    recognition.addEventListener("result", (e) => {
        let text = Array.from(e.results)
            .map((result) => result[0])
            .map((result) => result.transcript)
            .join("");

        
        currentText = text;
        
        if (e.results[0].isFinal) {
            //text = text.toLowerCase();
            console.log(text);
            /*output_text = output_text + " \n" + text;
            textarea.value = output_text;
            textarea.scrollTop = textarea.scrollHeight;*/
            output_text = output_text + text + "\n" ;
            textarea_G.scrollTop = textarea_G.scrollHeight;
            textarea_T.scrollTop = textarea_T.scrollHeight;
            textarea_H.scrollTop = textarea_T.scrollHeight;

        } else {
            console.log(text);
            textarea_T.value = output_text + currentText;
            textarea_T.scrollTop = textarea_T.scrollHeight;
            textarea_G.value = output_text + currentText;
            textarea_G.scrollTop = textarea_G.scrollHeight;
            textarea_H.value = output_text + currentText;
            textarea_H.scrollTop = textarea_G.scrollHeight;
        }
    });

    recognition.addEventListener("end", () => {
        if(state === 'sleep') {
            recognition.start();
        }
    });


    recognition.start();

    
    //EVENTS

    let currentTab = "Anrede 1";
    eventCount = 0;
    
    function shortcuts(e) {
        //console.log(e.key.toLowerCase())
        if (e.key == " " || e.code == "Space") {
            //document.getElementById("my_btn").click();
            console.log("Pressed Space")
        }
        if (e.key == "ArrowLeft") {
            console.log("Left Arrow pressed")
            
        }
        if (e.key == "ArrowRight") {
            //document.getElementById("my_btn").click();
            console.log("Right Arrow")
            console.log("Current Tab: " + currentTab);
            console.log("EventCount: " + eventCount);
            if (e.repeat) return;

            if(currentTab === "Anrede 1") {
                document.getElementById("Heimberg-button").click();
                return
            } else if(currentTab === "Heimberg") {
                if(eventCount === 0) {
                    document.getElementById("Heimberg-titleCard").style.display = "none";
                } else if(eventCount === 1) {
                    document.getElementById("Heimberg-webcam").style.display = "none";
                } else {
                    document.getElementById("Ratgeber Hausfrau-button").click();
                    return
                }
            } else if(currentTab === "Ratgeber Hausfrau") {
                if(eventCount === 0) {
                    document.getElementById("Ratgeber_Hausfrau-titleCard").style.display = "none";
                } else {
                    document.getElementById("Erfahrungen-button").click();
                    return
                }
            } else if(currentTab === "Erfahrungen") {
                document.getElementById("Stimmuntersuchung-button").click();
                return
            } else if(currentTab === "Stimmuntersuchung") {
                document.getElementById("Stimmuntersuchung-titleCard").style.display = "none";
            }

            eventCount++;
        }
    }  
    
    document.addEventListener('keydown', shortcuts, false);


    /*var buttonElement = document.getElementById("Heimberg-button");
    console.log(buttonElement)

    buttonElement.addEventListener("click", function() {
        // Your code to be executed when the button is clicked goes here
        console.log("Button clicked!");
    });*/

    var tabNav = document.querySelector('.tab-nav');

    console.log(tabNav);

    tabNav.addEventListener('click', function(event) {
        // Check if the clicked element is a button
        if (event.target && event.target.nodeName == 'BUTTON') {
            // Call your function here
            //console.log('Button clicked: ' + event.target.textContent);
            currentTab = event.target.textContent.trim();
            console.log("new tab selected: " + currentTab)
            eventCount = 0;
        }
    });

    //document.addEventListener(document.getElementById("Heimberg-button").click(), test, false);

    /*const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
    
    navigator.mediaDevices.getUserMedia = (constraints) => {
      if (!constraints.video.facingMode) {
        constraints.video.facingMode = {ideal: "environment"};
      }
      return originalGetUserMedia(constraints);
    };*/

    /*const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
    console.log("OriginalGetUserMedia: );
    console.log(originalGetUserMedia)*/

    
    /*navigator.mediaDevices.getUserMedia = (constraints) => {
      if (!constraints.video.facingMode) {
        constraints.video.facingMode = {ideal: "environment"};
      }
      return originalGetUserMedia(constraints);
    };*/

    /*console.log("Head skript")
    const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);

    console.log("Head skript2")
    navigator.mediaDevices.getUserMedia = async (constraints) => {
    try {
        // Check if constraints.video is defined and if deviceId is not set
        if (constraints.video && !constraints.video.deviceId) {
            // Get list of available media devices
            const devices = await navigator.mediaDevices.enumerateDevices();

            // Find the USB-C camera by checking its label or kind
            const usbCCamera = devices.find(device => 
                device.kind === 'videoinput' && 
                (device.label.includes('USB-C') || device.label.includes('your_device_label_here'))
            );
            console.log(devices)
            // If USB-C camera is found, set its deviceId in the constraints
            if (usbCCamera) {
                constraints.video.deviceId = { exact: usbCCamera.deviceId };
            }
            console.log(usbCCamera)
        }

        // Call the original getUserMedia with modified constraints
        return await originalGetUserMedia(constraints);
    } catch (error) {
        // Handle errors
        console.error('Error accessing media devices:', error);
        throw error;
    }
    };*/
    

}
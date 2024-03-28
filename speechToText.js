

function textToSpeech() {
    console.log("Js is loaded")
    var containerDiv_G = document.getElementById('speechToText_output_glimmer');
    var containerDiv_T = document.getElementById('speechToText_output_trigger');
    var containerDiv_H = document.getElementById('heimberg_textbox');
    var textarea_G = containerDiv_G.querySelector('[data-testid="textbox"]');
    var textarea_T = containerDiv_T.querySelector('[data-testid="textbox"]');
    var textarea_H = containerDiv_H.querySelector('[data-testid="textbox"]');
    textarea_T.style.textAlign = "center";
    textarea_T.style.fontSize = "20px";
    textarea_G.style.textAlign = "center";
    textarea_G.style.fontSize = "20px";
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

    //events when the left arrow is pressed 

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
        if (e.key == "ArrowUp") {
            //document.getElementById("my_btn").click();
            console.log("Right Arrow")
            console.log("Current Tab: " + currentTab);
            console.log("EventCount: " + eventCount);
            if (e.repeat) return;

            if(check_titleCard(currentTab)) return

            if(currentTab === "Anrede 1") {
                if(eventCount === 0) {
                    play_Video("Anrede 1_titleCard-Video");
                } else {
                    document.getElementById("Heimberg-button").click();
                    return
                }
                
            } else if(currentTab === "Heimberg") {
                if(eventCount === 0) {
                    document.getElementById("Heimberg-webcam").style.display = "none";
                    play_Video("Heimberg_Schweigen-Video");
                } else if(eventCount === 1) {
                    document.getElementById("Ratgeber Hausfrau-button").click();
                    return
                } 
            } else if(currentTab === "Ratgeber Hausfrau") {
                if(eventCount === 0) {
                    document.getElementById("Erfahrungen-button").click();
                    return
                }
            } else if(currentTab === "Erfahrungen") {
                document.getElementById("Stimmuntersuchung-button").click();
                return
            } else if(currentTab === "Stimmuntersuchung") {
                if(eventCount === 0) {
                    document.getElementById("Stimmuntersuchung-webcam").style.display = "none";
                } else if(eventCount === 1) {
                    document.getElementById("Anrede_2-button").click();
                    return
                }
            } else if(currentTab === "Anrede 2") {
                if(eventCount === 0) {
                    document.getElementById("Trigger-button").click();
                    return
                }
            } else if(currentTab === "Trigger") {
                if(eventCount === 0) {
                    document.getElementById("Gedicht-button").click();
                    return
                }
            } else if(currentTab === "Gedicht") {
                if(eventCount === 0) {
                    document.getElementById("Glimmer-button").click();
                    return
                }
            }

            eventCount++;
        }
    }  
    
    document.addEventListener('keydown', shortcuts, false);


    
    //Events that trigger when nav bar is changed TODO -> Play title card

    var tabNav = document.querySelector('.tab-nav');

    console.log(tabNav);

    tabNav.addEventListener('click', function(event) {
        // Check if the clicked element is a button
        if (event.target && event.target.nodeName == 'BUTTON') {
            // Call your function here
            //console.log('Button clicked: ' + event.target.textContent);
            currentTab = event.target.textContent.trim();
            console.log("new tab selected: " + currentTab)
            play_titleCard(currentTab);
            if(currentTab === "Heimberg" || currentTab === "Trigger" || currentTab === "Glimmer") {
                output_text = "";
                textarea_T.value = "";
                textarea_T.scrollTop = textarea_T.scrollHeight;
                textarea_G.value = "";
                textarea_G.scrollTop = textarea_G.scrollHeight;
                textarea_H.value = "";
                textarea_H.scrollTop = textarea_G.scrollHeight;
            }

            if(currentTab === "Heimberg") {
                activate_WebCam("Heimberg")
            }

            if(currentTab === "Ratgeber Hausfrau") {
                video_Loop("Ratgeber Hausfrau-Video");
            }

            if(currentTab === "Trigger") {
                video_Loop("Trigger-Video");
            }

            if(currentTab === "Glimmer") {
                video_Loop("Glimmer-Video");
            }

            if(currentTab === "Stimmuntersuchung") {
                activate_WebCam("Stimmuntersuchung");
            }
                
            eventCount = 0;
        }
    });

    
    //Video play 

    function video_Loop(name) {
        var parentDiv = document.getElementById(name);
        var video = parentDiv.querySelector("video");
        video.currentTime = 0;
        video.play();
    
        video.addEventListener("ended", function() {
            video.currentTime = 0; // Reset video to beginning
            video.play(); // Play the video again
        });
    }

    function play_titleCard(name) {
        var parentDiv = document.getElementById(name + "_titleCard-Video");
        var video = parentDiv.querySelector("video");

        //If commented out: Title wont be shown everytime tab is selected
        parentDiv.style.display = "block";
    
        video.play();
    
        video.addEventListener("ended", function() {
            parentDiv.style.display = "none";
        });
    }

    function play_Video(name) {
        var parentDiv = document.getElementById(name);
        var video = parentDiv.querySelector("video");


        //If commented out: Title wont be shown everytime tab is selected
        parentDiv.style.display = "block";
        video.currentTime = 0;
        video.play();
    
        video.addEventListener("ended", function() {
            parentDiv.style.display = "none";
        });
    }

    function check_titleCard(name) {
        var parentDiv = document.getElementById(name + "_titleCard-Video");
        var video = parentDiv.querySelector("video");

        if(parentDiv.style.display === "none") {
            return false;
        }
        parentDiv.style.display = "none";
        return true;
    }

    function activate_WebCam(name) {
        var parentDiv = document.getElementById(name + "-webcam");
        console.log(parentDiv)
        var webcam_Button = parentDiv.querySelector("button.svelte-qbrfs");
        console.log(webcam_Button)

        //If commented out: Title wont be shown everytime tab is selected
        parentDiv.style.display = "block";
    
        webcam_Button.click();
    }
    

}
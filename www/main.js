$(document).ready(function () {
    // Restore previous chat from localStorage if available
    const savedChat = localStorage.getItem("chatMemory");
    if (savedChat) {
        $('#Chatbox').val(savedChat);
        localStorage.removeItem("chatMemory"); // Optional: clear after restoring
    }

    // Textillate effect for any animated text
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" },
    });

    // Initialize SiriWave (but don't autostart yet)
    const siriWave = new SiriWave({
        container: document.getElementById('siriwave-container'),
        width: 800,
        height: 200,
        speed: 0.2,
        amplitude: 1,
        autostart: false
    });

    // Mic button click event
    $('#MicBtn').click(function () {
        console.log("Mic button clicked");

        const chatSection = document.getElementById("Oval");
        const siriWaveSection = document.getElementById("Siriwave");

        // Fade out chat and show SiriWave
        chatSection.classList.add('fade-out');
        setTimeout(() => {
            chatSection.style.display = "none";
            siriWaveSection.style.display = "block";
            siriWaveSection.classList.add('fade-in');
            siriWave.start();
        }, 500);

        // Start listening from Python backend (will use recognizer)
        setTimeout(() => {
            eel.allCommands()(function () {
                console.log("Voice command executed");
                // Hide SiriWave after execution
                siriWave.stop();
                siriWaveSection.classList.remove("fade-in");
                siriWaveSection.style.display = "none";

                chatSection.style.display = "block";
                chatSection.classList.remove("fade-out");
                chatSection.classList.add("fade-in");
            });
        }, 800);
    });

    $(document).ready(function () {
        const settingsBtn = document.getElementById("SettingsBtn"); // capital S
        const popup = document.getElementById("settingsPopup");
    
        if (settingsBtn && popup) {
            settingsBtn.addEventListener("click", () => {
                popup.classList.remove("hidden");
                popup.style.display = "block";
    
                setTimeout(() => {
                    popup.classList.add("hidden");
                    popup.style.display = "none";
                }, 5000);
            });
        }
    });
    
        });
    

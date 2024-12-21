// Configuración básica para reconocimiento de voz
const subtitulosDiv = document.getElementById('subtitulos');
const video = document.getElementById('video');
let recognition;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();

    // Configuración del reconocimiento
    recognition.continuous = true; // Reconocer en tiempo real
    recognition.lang = 'es-ES'; // Idioma del reconocimiento
    recognition.interimResults = true; // Mostrar resultados parciales

    console.log("Reconocimiento de voz configurado.");
} else {
    console.error("El reconocimiento de voz no es compatible con este navegador.");
}

// Función para iniciar reconocimiento cuando se reproduce el video
video.addEventListener('play', function () {
    if (recognition) {
        recognition.start();
        console.log("Reconocimiento de voz iniciado.");
    }
});

// Función para detener reconocimiento cuando se pausa el video
video.addEventListener('pause', function () {
    if (recognition) {
        recognition.stop();
        console.log("Reconocimiento de voz detenido.");
    }
});

// Mostrar subtítulos generados en tiempo real
if (recognition) {
    recognition.onresult = function (event) {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        subtitulosDiv.textContent = transcript;
        console.log("Subtítulos actualizados:", transcript);
    };

    recognition.onerror = function (event) {
        console.error("Error en reconocimiento de voz:", event.error);
    };
}

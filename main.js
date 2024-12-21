// Cargar video seleccionado
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const videoElement = document.getElementById('video');
        videoElement.src = URL.createObjectURL(file);
        videoElement.load();
    }
});

// Sincronizar subtítulos en tiempo real
const subtitulosDiv = document.getElementById('subtitulos');
const subtitulos = [
    { start: 0, end: 5, text: "Hola, bienvenidos al video." },
    { start: 6, end: 10, text: "Este es un generador de subtítulos." },
    { start: 11, end: 15, text: "Esperamos que lo disfrutes." }
];

document.getElementById('video').addEventListener('timeupdate', function() {
    const currentTime = this.currentTime;
    const subtituloActual = subtitulos.find(s => currentTime >= s.start && currentTime <= s.end);
    subtitulosDiv.textContent = subtituloActual ? subtituloActual.text : "";
});// Código JavaScript

let inactivityTime = function () {
    let time;
    const fullscreenImage = document.getElementById('fullscreenImage');

    // Funktionen zur Überwachung der Benutzerinteraktion
    window.onload = resetTimer;
    window.onmousemove = resetTimer;
    window.onkeydown = resetTimer;

    function showFullscreenImage() {
        fullscreenImage.style.display = 'flex';
    }

    function resetTimer() {
        clearTimeout(time);
        fullscreenImage.style.display = 'none';
        time = setTimeout(showFullscreenImage, 50000);
    }
};

// Starte die Überwachung der Inaktivität
inactivityTime();


const text = "Web Developer, Entrepreneur, Digitaler Pionier";
let index = 0;

function typeWriter() {
    if (index < text.length) {
        document.getElementById("typed-text").innerHTML += text.charAt(index);
        index++;
        setTimeout(typeWriter, 100);
    }
}

window.onload = typeWriter;
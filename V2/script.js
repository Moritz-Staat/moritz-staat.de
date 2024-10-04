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
        time = setTimeout(showFullscreenImage, 5000);
    }
};

// Starte die Überwachung der Inaktivität
inactivityTime();

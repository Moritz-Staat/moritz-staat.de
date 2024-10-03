let inactivityTime = function () {
    let time;
    const fullscreenImage = document.getElementById('fullscreenImage');

    // Funktionen zur Überwachung der Benutzerinteraktion
    window.onload = resetTimer;
    window.onmousemove = resetTimer;
    window.onkeydown = resetTimer;

    function showFullscreenImage() {
        fullscreenImage.style.display = 'flex';  // Bild im Vollbildmodus anzeigen
    }

    function resetTimer() {
        clearTimeout(time);
        fullscreenImage.style.display = 'none';  // Vollbildbild ausblenden, wenn Benutzer aktiv ist
        time = setTimeout(showFullscreenImage, 5000);  // Nach 30 Sekunden Inaktivität das Bild anzeigen
    }
};

// Starte die Überwachung der Inaktivität
inactivityTime();

let inactivityTime = function () {
    let time;
    let overlay = document.getElementById("inactiveOverlay");

    // Reset timer
    function resetTimer() {
        overlay.style.display = "none"; // Hide overlay
        clearTimeout(time);
        time = setTimeout(showOverlay, 60000);  // 1 Minute Inaktivität
    }

    // Show overlay after inactivity
    function showOverlay() {
        overlay.style.display = "flex";  // Show overlay
    }

    // Listen to activity events
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    document.ontouchstart = resetTimer; // for touch devices
};

inactivityTime();
